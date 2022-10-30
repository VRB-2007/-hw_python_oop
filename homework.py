from dataclasses import dataclass, astuple, fields


@dataclass
class InfoMessage:
    """Класс для создания объектов сообщений"""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFORMATION = ('Тип тренировки: {}; '
                   'Длительность: {:.3f} ч.; '
                   'Дистанция: {:.3f} км; '
                   'Ср. скорость: {:.3f} км/ч; '
                   'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.INFORMATION.format(*astuple(self))


@dataclass
class Training:
    """Базовый класс Training"""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

    action: int
    duration: float
    weight: float

    def get_distance(self):
        """Возвращает дистанцию, которую преодолели за тренировку"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        """Возвращает значение средней скорости движения во время тренировки"""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Возвращает количество килокал., потраченных за время тренировки"""
        pass

    def show_training_info(self) -> str:
        """Возвращает сообщение о тренировке"""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


@dataclass
class Running(Training):
    """Реализации классов-наследников class Running"""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):  # Расчёт калорий для этого класса
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    """Реализации классов-наследников class SportsWalking"""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    # Если менять название, то тесты выдают ошибку
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100
    height: float

    def get_spent_calories(self):
        """Расчёт калорий class SportsWalking"""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                    / (self.height / self.CM_IN_M))
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Реализации классов-наследников class Swimming"""
    LEN_STEP = 1.38
    CALORIES_WEIGHT_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    length_pool: float
    count_pool: int

    def get_mean_speed(self):
        """Возвращает значение средней скорости class Swimming"""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        """Расчёт калорий для этого класса"""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                * self.duration)


def main(training: Training):
    """Должна принимать на вход экземпляр класса Training"""
    print(training.show_training_info().get_message())


TRAINING_TIPES = {
    'SWM': (Swimming, len(fields(Swimming))),
    'RUN': (Running, len(fields(Running))),
    'WLK': (SportsWalking, len(fields(SportsWalking)))
}

ERROR_TRAINING_TEXT = 'Неизвестный код тренировки"{}".'
ERROR_PARAMS_TEXT = (
    'Неверное количество параметров для "{}".'
    ' требовалось {2}, а получили {1}.'
)


def read_package(work_type, data):
    """Принимает на вход код тренировки и список её параметров."""
    if work_type not in TRAINING_TIPES:
        raise NameError(ERROR_TRAINING_TEXT.format(work_type))
    if TRAINING_TIPES[work_type][1] != len(data):
        raise ValueError(ERROR_PARAMS_TEXT.format(work_type,
                                                  len(data),
                                                  TRAINING_TIPES[work_type][1])
                         )

    return TRAINING_TIPES[work_type][0](*data)


if __name__ == '__main__':

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
