import time
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
from model import SSD300, MultiBoxLoss
from datasets import PascalVOCDataset
from utils import *


data_folder = './'
keep_difficult = True


n_classes = len(label_map)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Параметры обучения
checkpoint = None
batch_size = 8  # размер партии
iterations = 80000  # количество итераций
workers = 4  # количество потоков загрузки ищзображений для DataLoader
print_freq = 200  # частота вывода информации при обучении
lr = 1e-3  # скорость обучения
decay_lr_at = [53000, 66000]  # номера итераций на которых уменьшается скорость обучения
decay_lr_to = 0.1  # на сколько уменьшать скорость обучения
momentum = 0.9  # импульс
weight_decay = 5e-4  # сокращение веса
grad_clip = None

cudnn.benchmark = True


def main():

    global start_epoch, label_map, epoch, checkpoint, decay_lr_at

    # Инициализация модели или загрузка чекпоинта
    if checkpoint is None:
        start_epoch = 0
        model = SSD300(n_classes=n_classes)
        biases = list()
        not_biases = list()
        for param_name, param in model.named_parameters():
            if param.requires_grad:
                if param_name.endswith('.bias'):
                    biases.append(param)
                else:
                    not_biases.append(param)
        optimizer = torch.optim.SGD(params=[{'params': biases, 'lr': 2 * lr}, {'params': not_biases}],
                                    lr=lr, momentum=momentum, weight_decay=weight_decay)

    else:
        checkpoint = torch.load(checkpoint)
        start_epoch = checkpoint['epoch'] + 1
        print('\nLoaded checkpoint from epoch %d.\n' % start_epoch)
        model = checkpoint['model']
        optimizer = checkpoint['optimizer']

    model = model.to(device)
    criterion = MultiBoxLoss(priors_cxcy=model.priors_cxcy).to(device)

    # Загрузчики данных
    train_dataset = PascalVOCDataset(data_folder,
                                     split='train',
                                     keep_difficult=keep_difficult)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                                               collate_fn=train_dataset.collate_fn, num_workers=workers,
                                               pin_memory=True)

    # Вычисление количесвта эпох
    epochs = iterations // (len(train_dataset) // batch_size)
    decay_lr_at = [it // (len(train_dataset) // batch_size) for it in decay_lr_at]

    # Эпохи
    for epoch in range(start_epoch, epochs):

        # Уменьшение скорости обучения
        if epoch in decay_lr_at:
            adjust_learning_rate(optimizer, decay_lr_to)

        # OОбучение в течении одной эпохи
        train(train_loader=train_loader,
              model=model,
              criterion=criterion,
              optimizer=optimizer,
              epoch=epoch)

        # Сохранение чекпоинта
        save_checkpoint(epoch, model, optimizer)


def train(train_loader, model, criterion, optimizer, epoch):

    model.train()

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()

    start = time.time()

    # Партии изображений
    for i, (images, boxes, labels, _) in enumerate(train_loader):
        data_time.update(time.time() - start)

        images = images.to(device)
        boxes = [b.to(device) for b in boxes]
        labels = [l.to(device) for l in labels]

        # Прямое распространение
        predicted_locs, predicted_scores = model(images)

        # Потери
        loss = criterion(predicted_locs, predicted_scores, boxes, labels)

        # Обратное распртранение
        optimizer.zero_grad()
        loss.backward()

        if grad_clip is not None:
            clip_gradient(optimizer, grad_clip)

        # Обновление модели
        optimizer.step()

        losses.update(loss.item(), images.size(0))
        batch_time.update(time.time() - start)

        start = time.time()

        # Вывод статуса
        if i % print_freq == 0:
            print('Epoch: [{0}][{1}/{2}]\t'
                  'Batch Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                  'Data Time {data_time.val:.3f} ({data_time.avg:.3f})\t'
                  'Loss {loss.val:.4f} ({loss.avg:.4f})\t'.format(epoch, i, len(train_loader),
                                                                  batch_time=batch_time,
                                                                  data_time=data_time, loss=losses))
    del predicted_locs, predicted_scores, images, boxes, labels  # Очистка памяти


if __name__ == '__main__':
    main()
