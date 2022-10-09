class InfoMessage:
    """Класс для создания объектов сообщений"""
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Возвращает строку сообщения"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс Training"""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

    def __init__(self, action: int, duration: float, weight: float):
        """Конструктор должен получать информацию с датчиков"""
        self.action = action
        self.duration = duration
        self.weight = weight

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
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Реализации классов-наследников class Running"""
    def get_spent_calories(self):  # Расчёт калорий для этого класса
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        mean_speed: float = self.get_mean_speed()
        spent_calories: float = ((coeff_calorie_1 * mean_speed
                                  - coeff_calorie_2) * self.weight
                                 / self.M_IN_KM * self.duration
                                 * self.MIN_IN_H)
        return spent_calories


class SportsWalking(Training):
    """Реализации классов-наследников class SportsWalking"""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Расчёт калорий class SportsWalking"""
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        mean_speed: float = self.get_mean_speed()
        return ((coeff_calorie_1 * self.weight
                + (mean_speed ** 2 // self.height)
                * coeff_calorie_2 * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Реализации классов-наследников class Swimming"""
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float, count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Возвращает значение средней скорости class Swimming"""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        """Расчёт калорий для этого класса"""
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        mean_speed: float = self.get_mean_speed()
        spent_calories: float = ((mean_speed + coeff_calorie_1)
                                 * coeff_calorie_2 * self.weight)
        return spent_calories


def main(training: Training):
    """Должна принимать на вход экземпляр класса Training"""
    info = training.show_training_info()
    print(info.get_message())


def read_package(workout_type, data):
    """Принимает на вход код тренировки и список её параметров."""
    training_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    return training_type[workout_type](*data)


if __name__ == '__main__':

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
