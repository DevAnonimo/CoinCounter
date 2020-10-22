import cv2
import numpy as np

path = 'images/moedas1.jpg'
nome_saida = 'imagem2'
path_saida = 'images/'+nome_saida+'.jpg'

def detect_coins():
    coins = cv2.imread(path, 1)

    gray = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(gray, 7)
    circles = cv2.HoughCircles(
        img,  # source image
        cv2.HOUGH_GRADIENT,  # type of detection
        1,
        50,
        param1=100,
        param2=50,
        minRadius=10,  # minimal radius
        maxRadius=380,  # max radius
    )

    coins_copy = coins.copy()


    for detected_circle in circles[0]:
        x_coor, y_coor, detected_radius = detected_circle
        coins_detected = cv2.circle(
            coins_copy,
            (int(x_coor), int(y_coor)),
            int(detected_radius),
            (0, 255, 0),
            4,
        )

    cv2.imwrite(path_saida, coins_detected)

    return circles

def calculate_amount():
    koruny = {
        "R$ 0,01": {
            "value": 0.01,
            "radius": 20,
            "ratio": 1,
            "count": 0,
        },
        "R$ 0,10": {
            "value": 0.1,
            "radius": 21.5,
            "ratio": 1.075,
            "count": 0,
        },
        "R$ 0,05": {
            "value": 0.05,
            "radius": 23,
            "ratio": 1.15,
            "count": 0,
        },
        "R$ 0,25": {
            "value": 0.25,
            "radius": 26,
            "ratio": 1.3,
            "count": 0,
        },
        "R$ 1,00": {
            "value": 1,
            "radius": 27.5,
            "ratio": 1.375,
            "count": 0,
        },
    }

    circles = detect_coins()
    radius = []
    coordinates = []

    for detected_circle in circles[0]:
        x_coor, y_coor, detected_radius = detected_circle
        radius.append(detected_radius)
        coordinates.append([x_coor, y_coor])

    smallest = min(radius)
    tolerance = 0.0375
    total_amount = 0

    coins_circled = cv2.imread(path, 1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    for coin in circles[0]:
        ratio_to_check = coin[2] / smallest
        coor_x = coin[0]
        coor_y = coin[1]
        for koruna in koruny:
            value = koruny[koruna]['value']
            if abs(ratio_to_check - koruny[koruna]['ratio']) <= tolerance:
                koruny[koruna]['count'] += 1
                total_amount += koruny[koruna]['value']
                cv2.putText(coins_circled, str(value), (int(coor_x), int(coor_y)), font, 1,
                            (0, 0, 0), 4)

    print(f"O valor total é R$ {total_amount:.2f}")
    for koruna in koruny:
        pieces = koruny[koruna]['count']
        print(f"{koruna} = {pieces}x")


    cv2.imwrite(path_saida, coins_circled)
    resultado = cv2.imread(path_saida, 1)
    cv2.imshow('Resultado',resultado)



if __name__ == "__main__":
    calculate_amount()
