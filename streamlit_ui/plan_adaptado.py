import json
import streamlit as st
from streamlit_lottie import st_lottie
from interfaces.generador_textos import GeneradorTextos
from modelos.modelo_gpt import ModeloGPT
from analisis.EnriquecerPeticionUsuario import procesar_peticion, obtener_ubicacion, obtener_hora_local
import re
import folium
from streamlit_folium import folium_static
import os

def mostrar_animacion_lottie():
    """
    Muestra el título con la animación Lottie al lado.
    """
    # Animación Lottie incrustada como diccionario
    animacion = {
        "v": "5.10.0",
        "fr": 29.9700012207031,
        "ip": 0,
        "op": 40.0000016292334,
        "w": 1500,
        "h": 1500,
        "nm": "character",
        "ddd": 0,
        "assets": [
            {
                "id": "image_0",
                "w": 132,
                "h": 153,
                "u": "",
                "p": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIQAAACZBAMAAAAcIo/RAAAAJHpUWHRDcmVhdG9yAAAImXNMyU9KVXBMK0ktUnBNS0tNLikGAEF6Bs5qehXFAAAACXBIWXMAAAABAAAAAQBPJcTWAAAAG1BMVEVHcEzz0qX00qX01KTvz6Pz0qXz0qby0qbz0qXcs91WAAAACHRSTlMAxX87FeupWapFohIAAAKZSURBVGje7ZpLT9tAFIUdbDDLNrQoS0Sp6qXVKi1Lt4jHMhJdZAlqK3kZVS1iGwc792eX0KBk8Hg895xWAuTzAz7N3Mc87r1B0Kij/cuXS/XfpYFe71+Lod1fSsBpLjX1VSu5EpvKA29A9FYa9I0miOzQBJFXPojf4pSHPU7cBCknbYR43IKQKmsxRC6tOncjPouHnFsJxz6IyoW4Fi99d9jSjyDTjF2EI8B8F+FYhvciRC4YdzidciwK2WNjoEHMbIQNDUHKjDNmg0GjsQ5R1BFbOoJtJ4dKhGUnYy1ixvnjLsipuLJHV6JHjDiXLjRH83zNrSZiE0BIykVFPTJyBHFjWBMhmGkSQ4gpk2NLrWfaNobYw48bm0sSDDFCT155vmOEda+GIKJizptaYKAIWSF6KCLjESkbnOvHJ4xYRfgZjzh82ogXHeIZI44SFLGzTNWPguvvH3xDGJUpeqkbF0HMERZP2E0ScXsrXrOIG9YUi4ffgEUUHaJDdIgngUhYxAy/hlZv+R6LmECf3IeP6CGHWFRJQsonxd0bOv6BE/pZ98rpEP8DcfHIvjTbjwIBv/rSf/lb3kIRfOWgZMtaRv0iAhEFU/i9f/iSVUKzTgherCO23GlW18DwnARsYBjFX6w2VnHl/Ic+BV1i1tLPuNMCzlWzQxLS1oSKpjO2SVNv0/RYUyDGqPcA1fn+NaA7PXsB22+asl1Ie6v8mN2H9iaw92QTzh/aVCvtQyXRAD1tlAMH9YMXa3HPG7v9Q3YR/taYs+MX7lmSKEdjW5ds05ZhlCGWHbqtnLfO5bRN1RRZ+2zPF7chvCauTlB/ejF8Cbd7abBHpZgbi3Pn79pvaOuqtpDqIFAq+mmM0O2+CRCFn/aX+uDawh+LQ+fajeAipwAAAABJRU5ErkJggg==",
                "e": 1
            },
            {
                "id": "image_1",
                "w": 92,
                "h": 52,
                "u": "",
                "p": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFwAAAA0BAMAAAD1ZkJcAAAAJHpUWHRDcmVhdG9yAAAImXNMyU9KVXBMK0ktUnBNS0tNLikGAEF6Bs5qehXFAAAACXBIWXMAAAABAAAAAQBPJcTWAAAAHlBMVEVHcEzlnlzmnV7lnl3lnl3mn2Dfn2Dmnl3mnl7lnl0Pc8+CAAAACXRSTlMAT3672SYQmvBkCt0WAAABWklEQVRIx7WWy0/CQBDGt4aqx4KveBM0QW6+ouHmIyHpDYwXb8jJIyTWhKuJJr2prZH5b11aKGXZxzcHv2t/+2U6MzuzQqjq1Q7PMzXqXeGQ1wyppLt63wa/kKp0ZDqwvkU6Jbt66zEZdKqhByEZdbsS0CAmi94Ufs1Kq7wXkkM35ZyMyanLBf7gpiktSuzFAE5fc3yfIAUzc4ye24PmM3s/Jo59BaUpndaqBeM0lCWKcfxHdgtO068Qmwyc+nga81S2OPhQtDn4CQ//FOG/4qxgrrm/ykrkgXjk4F1G/8oOxq/eVN+y3xmZ/OBc1fyybsB0kk08OJpONjieQXqSjz10crwzJmphLqNv45FnuwObAoW23fUPytvm2IW/Lq0y37FuImVR2vloZQ37R+YURrotv2coVxLADw5pPTK/Ue4v1Pyd2Z9AT83FicmV+70kf7paa0hVdzTf/gDPpEYS8LYM6AAAAABJRU5ErkJggg==",
                "e": 1
            },
            {
                "id": "image_2",
                "w": 174,
                "h": 215,
                "u": "",
                "p": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK4AAADXBAMAAABxD3fUAAAAJHpUWHRDcmVhdG9yAAAImXNMyU9KVXBMK0ktUnBNS0tNLikGAEF6Bs5qehXFAAAACXBIWXMAAAABAAAAAQBPJcTWAAAAG1BMVEVHcEz/AAL/AAT/AAD/AAT/AAP/AAP/AAL/AANwPGeKAAAACHRSTlMAwoUYPeqhZkdxueQAAALeSURBVHja7ZzNTxNRFMUfTqEuoSQ6S6wYWT4JGpdoinRJgOAsa5DYZYOBdOlUZ3r/bHFay3Q+38e5C5J7/oBfXu47973NPVepZg36r3bK6u8fKw+dfouoTvEPR3RwH1KzXvx0wN5G1K5z2zN3bshIyXcr7JeITHVlfuTgjiyUmFY5uCErJddm2DHZ6poHawJ2whqA75ywlOw1Yz+Ro+JGux2Ss2a6octCdy5d1nOn5KPaEn/wwlKsGarQUIkTTywllZ7okrfm+EurvbotAJbSMneM4NKoiH0GwZYPPMVwaQI3Q6UlTlBcWvNwEMG4F3nuBgxLcZ57gOPme6MDxNKfR+57JDfRLGXIFQJahlwhNrDclSOGWO6qlyMw9wz8NhTeiE00N8E+kcUCh3DuNoN7Vw7ewnNTlmtbXtwQz80+jTEDd8TQbcuOY7BDZoguB3fGYrPMaJsc3AejfeTgkmax7z8DT1m4e+C/+JE7ZuFuM7y+T5F7xsT9JVzhCle4whWucIUrXOEKV7jCFa5whStc4QpXuMIVrnCFK1zhCle4whWucIUrXOEKV7gFbiR1oKc4t3LAwh2xzRsNWbhjtnmu5yxc+LDyQjEsyLCulGnOca5UwMH9zTL+uxgAnrLYl2fQUStWosUsY+bLQXNgluS/LhiyDItXUrFcnFasA+HLcFLA0W2KYXJ7xBFvWZUX/lTOVrmZiMG9+JH7Y3T4rVgHFYQsZUDG1NaDasA3bc6QWsw3BTjyFBfi16ib2y3kIUG9nBQzvR1Mz12i07zZccuJXsiBqxLI7wBmqAogAyyxW5mX9v7nUs0RRy9lblFX1x+g9wq6xxq+9SDT7qRpS0MIdoN3ib+27H9w3KjQtE3B4+7SVqwTODbaYWINTg1XoxzaXd65Vobq2tjtpTH2wcdfjNvh9d1Cm88WR+5ZL/cJ7turvOWy2EcFt81n7jlRMx31d2oc29vXyk9Hg9P+mt4OBu3Mv2AJOXY7WXg7CQAAAABJRU5ErkJggg==",
                "e": 1
            }
        ],
        "layers": [
            {
                "ddd": 0,
                "ind": 1,
                "ty": 2,
                "nm": "face",
                "parent": 3,
                "refId": "image_0",
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100, "ix": 11},
                    "r": {
                        "a": 1,
                        "k": [
                            {"i": {"x": [0.667], "y": [1]}, "o": {"x": [0.333], "y": [0]}, "t": 0, "s": [-14]},
                            {"i": {"x": [0.667], "y": [1]}, "o": {"x": [0.333], "y": [0]}, "t": 20, "s": [14]},
                            {"t": 40.0000016292334, "s": [-14]}
                        ],
                        "ix": 10
                    },
                    "p": {"a": 0, "k": [87, 21.012, 0], "ix": 2, "l": 2},
                    "a": {"a": 0, "k": [62.923, 153, 0], "ix": 1, "l": 2},
                    "s": {"a": 0, "k": [100, 100, 100], "ix": 6, "l": 2}
                },
                "ao": 0,
                "ip": 0,
                "op": 150.000006109625,
                "st": 0,
                "bm": 0
            },
            {
                "ddd": 0,
                "ind": 2,
                "ty": 2,
                "nm": "neck",
                "parent": 3,
                "refId": "image_1",
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100, "ix": 11},
                    "r": {"a": 0, "k": 0, "ix": 10},
                    "p": {"a": 0, "k": [89.948, 12.099, 0], "ix": 2, "l": 2},
                    "a": {"a": 0, "k": [45.545, 25.815, 0], "ix": 1, "l": 2},
                    "s": {"a": 0, "k": [100, 100, 100], "ix": 6, "l": 2}
                },
                "ao": 0,
                "ip": 0,
                "op": 150.000006109625,
                "st": 0,
                "bm": 0
            },
            {
                "ddd": 0,
                "ind": 3,
                "ty": 2,
                "nm": "body",
                "refId": "image_2",
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100, "ix": 11},
                    "r": {"a": 0, "k": 0, "ix": 10},
                    "p": {
                        "a": 1,
                        "k": [
                            {"i": {"x": 0.667, "y": 1}, "o": {"x": 0.333, "y": 0}, "t": 0, "s": [792.694, 860.66, 0], "to": [-6.667, -6.2, 0], "ti": [14.667, 0, 0]},
                            {"i": {"x": 0.667, "y": 1}, "o": {"x": 0.333, "y": 0}, "t": 10, "s": [752.694, 823.46, 0], "to": [-14.667, 0, 0], "ti": [0, 0, 0]},
                            {"i": {"x": 0.667, "y": 1}, "o": {"x": 0.333, "y": 0}, "t": 20, "s": [704.694, 860.66, 0], "to": [0, 0, 0], "ti": [-14.667, 0, 0]},
                            {"i": {"x": 0.667, "y": 1}, "o": {"x": 0.333, "y": 0}, "t": 30, "s": [752.694, 823.46, 0], "to": [14.667, 0, 0], "ti": [-6.667, -6.2, 0]},
                            {"t": 40.0000016292334, "s": [792.694, 860.66, 0]}
                        ],
                        "ix": 2,
                        "l": 2
                    },
                    "a": {"a": 0, "k": [87, 179.261, 0], "ix": 1, "l": 2},
                    "s": {"a": 0, "k": [146, 146, 100], "ix": 6, "l": 2}
                },
                "ao": 0,
                "ip": 0,
                "op": 150.000006109625,
                "st": 0,
                "bm": 0
            },
            {
                "ddd": 0,
                "ind": 4,
                "ty": 4,
                "nm": "leg",
                "parent": 3,
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100, "ix": 11},
                    "r": {"a": 0, "k": 0, "ix": 10},
                    "p": {"a": 0, "k": [114.445, 215, 0], "ix": 2, "l": 2},
                    "a": {"a": 0, "k": [-39, 102.6, 0], "ix": 1, "l": 2},
                    "s": {"a": 0, "k": [89, 89, 100], "ix": 6, "l": 2}
                },
                "ao": 0,
                "shapes": [
                    {
                        "ty": "gr",
                        "it": [
                            {
                                "ind": 0,
                                "ty": "sh",
                                "ix": 1,
                                "ks": {
                                    "a": 1,
                                    "k": [
                                        {"i": {"x": 0.833, "y": 0.833}, "o": {"x": 0.766, "y": 0}, "t": 0, "s": [{"i": [[-178.326, -74.539], [12.787, -60.034]], "o": [[167.09, 94.764], [-9.685, 23.112]], "v": [[-39, 80.517], [-42, 287]], "c": False}]},
                                        {"i": {"x": 0.428, "y": 1}, "o": {"x": 0.167, "y": 0.167}, "t": 10, "s": [{"i": [[-178.326, -74.539], [-14.461, -57.225]], "o": [[51.744, 108.555], [-5.753, 21.989]], "v": [[-39, 80.517], [44.517, 306.663]], "c": False}]},
                                        {"i": {"x": 0.833, "y": 0.833}, "o": {"x": 0.6, "y": 0}, "t": 20, "s": [{"i": [[-178.326, -74.539], [-41.708, -54.416]], "o": [[93.494, 112.18], [-1.82, 20.865]], "v": [[-39, 80.517], [131.034, 290.371]], "c": False}]},
                                        {"i": {"x": 0.428, "y": 1}, "o": {"x": 0.167, "y": 0.167}, "t": 30, "s": [{"i": [[-178.326, -74.539], [-14.461, -57.225]], "o": [[130.292, 103.472], [-5.753, 21.989]], "v": [[-39, 80.517], [44.517, 306.663]], "c": False}]},
                                        {"t": 40.0000016292334, "s": [{"i": [[-178.326, -74.539], [12.787, -60.034]], "o": [[167.09, 94.764], [-9.685, 23.112]], "v": [[-39, 80.517], [-42, 287]], "c": False}]}
                                    ],
                                    "ix": 2
                                },
                                "nm": "Path 1",
                                "mn": "ADBE Vector Shape - Group",
                                "hd": False
                            },
                            {
                                "ty": "st",
                                "c": {"a": 0, "k": [1, 0, 0.011764706817, 1], "ix": 3},
                                "o": {"a": 0, "k": 100, "ix": 4},
                                "w": {"a": 0, "k": 60, "ix": 5},
                                "lc": 2,
                                "lj": 1,
                                "ml": 4,
                                "bm": 0,
                                "nm": "Stroke 1",
                                "mn": "ADBE Vector Graphic - Stroke",
                                "hd": False
                            },
                            {
                                "ty": "tr",
                                "p": {"a": 0, "k": [0, 0], "ix": 2},
                                "a": {"a": 0, "k": [0, 0], "ix": 1},
                                "s": {"a": 0, "k": [100, 100], "ix": 3},
                                "r": {"a": 0, "k": 0, "ix": 6},
                                "o": {"a": 0, "k": 100, "ix": 7},
                                "sk": {"a": 0, "k": 0, "ix": 4},
                                "sa": {"a": 0, "k": 0, "ix": 5},
                                "nm": "Transform"
                            }
                        ],
                        "nm": "Shape 1",
                        "np": 3,
                        "cix": 2,
                        "bm": 0,
                        "ix": 1,
                        "mn": "ADBE Vector Group",
                        "hd": False
                    }
                ],
                "ip": 0,
                "op": 150.000006109625,
                "st": 0,
                "ct": 1,
                "bm": 0
            },
            {
                "ddd": 0,
                "ind": 5,
                "ty": 4,
                "nm": "leg",
                "parent": 3,
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100, "ix": 11},
                    "r": {"a": 0, "k": 0, "ix": 10},
                    "p": {"a": 0, "k": [52.445, 215, 0], "ix": 2, "l": 2},
                    "a": {"a": 0, "k": [-39, 102.6, 0], "ix": 1, "l": 2},
                    "s": {"a": 0, "k": [89, 89, 100], "ix": 6, "l": 2}
                },
                "ao": 0,
                "shapes": [
                    {
                        "ty": "gr",
                        "it": [
                            {
                                "ind": 0,
                                "ty": "sh",
                                "ix": 1,
                                "ks": {
                                    "a": 1,
                                    "k": [
                                        {"i": {"x": 0.833, "y": 0.833}, "o": {"x": 0.766, "y": 0}, "t": 0, "s": [{"i": [[0, 0], [0, 0]], "o": [[0, 0], [0, 0]], "v": [[-39, 85.011], [-172.337, 287]], "c": False}]},
                                        {"i": {"x": 0.428, "y": 1}, "o": {"x": 0.167, "y": 0.167}, "t": 10, "s": [{"i": [[0, 0], [-3.719, -45.185]], "o": [[-28.039, 66.851], [2.021, 24.559]], "v": [[-37.315, 82.202], [-120.652, 304.978]], "c": False}]},
                                        {"i": {"x": 0.833, "y": 0.833}, "o": {"x": 0.6, "y": 0}, "t": 20, "s": [{"i": [[0, 0], [-7.438, -90.371]], "o": [[-196.955, 83.528], [4.043, 49.118]], "v": [[-35.629, 79.393], [-68.966, 287]], "c": False}]},
                                        {"i": {"x": 0.428, "y": 1}, "o": {"x": 0.167, "y": 0.167}, "t": 30, "s": [{"i": [[0, 0], [-3.719, -45.185]], "o": [[-98.478, 41.764], [2.021, 24.559]], "v": [[-37.315, 82.202], [-120.652, 304.978]], "c": False}]},
                                        {"t": 40.0000016292334, "s": [{"i": [[0, 0], [0, 0]], "o": [[0, 0], [0, 0]], "v": [[-39, 85.011], [-172.337, 287]], "c": False}]}
                                    ],
                                    "ix": 2
                                },
                                "nm": "Path 1",
                                "mn": "ADBE Vector Shape - Group",
                                "hd": False
                            },
                            {
                                "ty": "st",
                                "c": {"a": 0, "k": [1, 0, 0.011764706817, 1], "ix": 3},
                                "o": {"a": 0, "k": 100, "ix": 4},
                                "w": {"a": 0, "k": 60, "ix": 5},
                                "lc": 2,
                                "lj": 1,
                                "ml": 4,
                                "bm": 0,
                                "nm": "Stroke 1",
                                "mn": "ADBE Vector Graphic - Stroke",
                                "hd": False
                            },
                            {
                                "ty": "tr",
                                "p": {"a": 0, "k": [0, 0], "ix": 2},
                                "a": {"a": 0, "k": [0, 0], "ix": 1},
                                "s": {"a": 0, "k": [100, 100], "ix": 3},
                                "r": {"a": 0, "k": 0, "ix": 6},
                                "o": {"a": 0, "k": 100, "ix": 7},
                                "sk": {"a": 0, "k": 0, "ix": 4},
                                "sa": {"a": 0, "k": 0, "ix": 5},
                                "nm": "Transform"
                            }
                        ],
                        "nm": "Shape 1",
                        "np": 3,
                        "cix": 2,
                        "bm": 0,
                        "ix": 1,
                        "mn": "ADBE Vector Group",
                        "hd": False
                    }
                ],
                "ip": 0,
                "op": 150.000006109625,
                "st": 0,
                "ct": 1,
                "bm": 0
            },
            {
                "ddd": 0,
                "ind": 6,
                "ty": 4,
                "nm": "hand 2",
                "parent": 3,
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100, "ix": 11},
                    "r": {"a": 0, "k": 0, "ix": 10},
                    "p": {"a": 0, "k": [152.155, 46.686, 0], "ix": 2, "l": 2},
                    "a": {"a": 0, "k": [-236, -49, 0], "ix": 1, "l": 2},
                    "s": {"a": 0, "k": [100, 100, 100], "ix": 6, "l": 2}
                },
                "ao": 0,
                "shapes": [
                    {
                        "ty": "gr",
                        "it": [
                            {
                                "ind": 0,
                                "ty": "sh",
                                "ix": 1,
                                "ks": {
                                    "a": 1,
                                    "k": [
                                        {"i": {"x": 0.833, "y": 0.833}, "o": {"x": 0.766, "y": 0}, "t": 0, "s": [{"i": [[0, 0], [121, 41]], "o": [[80, -23], [0, 0]], "v": [[-207, 63], [-236, -45]], "c": False}]},
                                        {"i": {"x": 0.428, "y": 1}, "o": {"x": 0.167, "y": 0.167}, "t": 10, "s": [{"i": [[0, 0], [65.006, -2.724]], "o": [[-75.027, -3.97], [0, 0]], "v": [[-57.973, -40.03], [-236, -45]], "c": False}]},
                                        {"i": {"x": 0.833, "y": 0.833}, "o": {"x": 0.6, "y": 0}, "t": 20, "s": [{"i": [[0, 0], [81, -29]], "o": [[-78, 33], [0, 0]], "v": [[-23, -129], [-236, -45]], "c": False}]},
                                        {"i": {"x": 0.428, "y": 1}, "o": {"x": 0.167, "y": 0.167}, "t": 30, "s": [{"i": [[0, 0], [65.006, -2.724]], "o": [[-75.027, -3.97], [0, 0]], "v": [[-57.973, -40.03], [-236, -45]], "c": False}]},
                                        {"t": 40.0000016292334, "s": [{"i": [[0, 0], [121, 41]], "o": [[80, -23], [0, 0]], "v": [[-207, 63], [-236, -45]], "c": False}]}
                                    ],
                                    "ix": 2
                                },
                                "nm": "Path 1",
                                "mn": "ADBE Vector Shape - Group",
                                "hd": False
                            },
                            {
                                "ty": "st",
                                "c": {"a": 0, "k": [0.952941236309, 0.823529471603, 0.647058823529, 1], "ix": 3},
                                "o": {"a": 0, "k": 100, "ix": 4},
                                "w": {"a": 0, "k": 45, "ix": 5},
                                "lc": 2,
                                "lj": 1,
                                "ml": 4,
                                "bm": 0,
                                "nm": "Stroke 1",
                                "mn": "ADBE Vector Graphic - Stroke",
                                "hd": False
                            },
                            {
                                "ty": "tr",
                                "p": {"a": 0, "k": [0, 0], "ix": 2},
                                "a": {"a": 0, "k": [0, 0], "ix": 1},
                                "s": {"a": 0, "k": [100, 100], "ix": 3},
                                "r": {"a": 0, "k": 0, "ix": 6},
                                "o": {"a": 0, "k": 100, "ix": 7},
                                "sk": {"a": 0, "k": 0, "ix": 4},
                                "sa": {"a": 0, "k": 0, "ix": 5},
                                "nm": "Transform"
                            }
                        ],
                        "nm": "Shape 1",
                        "np": 3,
                        "cix": 2,
                        "bm": 0,
                        "ix": 1,
                        "mn": "ADBE Vector Group",
                        "hd": False
                    }
                ],
                "ip": 0,
                "op": 150.000006109625,
                "st": 0,
                "ct": 1,
                "bm": 0
            },
            {
                "ddd": 0,
                "ind": 7,
                "ty": 4,
                "nm": "hand",
                "parent": 3,
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100, "ix": 11},
                    "r": {"a": 0, "k": 0, "ix": 10},
                    "p": {"a": 0, "k": [23.155, 46.686, 0], "ix": 2, "l": 2},
                    "a": {"a": 0, "k": [-85, -49, 0], "ix": 1, "l": 2},
                    "s": {"a": 0, "k": [100, 100, 100], "ix": 6, "l": 2}
                },
                "ao": 0,
                "shapes": [
                    {
                        "ty": "gr",
                        "it": [
                            {
                                "ind": 0,
                                "ty": "sh",
                                "ix": 1,
                                "ks": {
                                    "a": 1,
                                    "k": [
                                        {"i": {"x": 0.833, "y": 0.833}, "o": {"x": 0.766, "y": 0}, "t": 0, "s": [{"i": [[0, 0], [0, 0]], "o": [[-118, -57], [0, 0]], "v": [[-85, -49], [-281, -149]], "c": False}]},
                                        {"i": {"x": 0.428, "y": 1}, "o": {"x": 0.167, "y": 0.167}, "t": 10, "s": [{"i": [[0, 0], [0, 0]], "o": [[-122, 14.99], [0, 0]], "v": [[-85, -48.99], [-217.42, 25.016]], "c": False}]},
                                        {"i": {"x": 0.833, "y": 0.833}, "o": {"x": 0.6, "y": 0}, "t": 20, "s": [{"i": [[0, 0], [0, 0]], "o": [[-218, 55], [0, 0]], "v": [[-85, -48], [-118, 59]], "c": False}]},
                                        {"i": {"x": 0.428, "y": 1}, "o": {"x": 0.167, "y": 0.167}, "t": 30, "s": [{"i": [[0, 0], [0, 0]], "o": [[-122, 14.99], [0, 0]], "v": [[-85, -48.99], [-217.42, 25.016]], "c": False}]},
                                        {"t": 40.0000016292334, "s": [{"i": [[0, 0], [0, 0]], "o": [[-118, -57], [0, 0]], "v": [[-85, -49], [-281, -149]], "c": False}]}
                                    ],
                                    "ix": 2
                                },
                                "nm": "Path 1",
                                "mn": "ADBE Vector Shape - Group",
                                "hd": False
                            },
                            {
                                "ty": "st",
                                "c": {"a": 0, "k": [0.952941236309, 0.823529471603, 0.647058823529, 1], "ix": 3},
                                "o": {"a": 0, "k": 100, "ix": 4},
                                "w": {"a": 0, "k": 45, "ix": 5},
                                "lc": 2,
                                "lj": 1,
                                "ml": 4,
                                "bm": 0,
                                "nm": "Stroke 1",
                                "mn": "ADBE Vector Graphic - Stroke",
                                "hd": False
                            },
                            {
                                "ty": "tr",
                                "p": {"a": 0, "k": [0, 0], "ix": 2},
                                "a": {"a": 0, "k": [0, 0], "ix": 1},
                                "s": {"a": 0, "k": [100, 100], "ix": 3},
                                "r": {"a": 0, "k": 0, "ix": 6},
                                "o": {"a": 0, "k": 100, "ix": 7},
                                "sk": {"a": 0, "k": 0, "ix": 4},
                                "sa": {"a": 0, "k": 0, "ix": 5},
                                "nm": "Transform"
                            }
                        ],
                        "nm": "Shape 1",
                        "np": 3,
                        "cix": 2,
                        "bm": 0,
                        "ix": 1,
                        "mn": "ADBE Vector Group",
                        "hd": False
                    }
                ],
                "ip": 0,
                "op": 150.000006109625,
                "st": 0,
                "ct": 1,
                "bm": 0
            },
            {
                "ddd": 0,
                "ind": 8,
                "ty": 4,
                "nm": "platform",
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100, "ix": 11},
                    "r": {"a": 0, "k": 0, "ix": 10},
                    "p": {"a": 0, "k": [744.267, 1187.168, 0], "ix": 2, "l": 2},
                    "a": {"a": 0, "k": [-3, 289, 0], "ix": 1, "l": 2},
                    "s": {"a": 0, "k": [148.995, 118.649, 100], "ix": 6, "l": 2}
                },
                "ao": 0,
                "shapes": [
                    {
                        "ty": "gr",
                        "it": [
                            {
                                "ind": 0,
                                "ty": "sh",
                                "ix": 1,
                                "ks": {
                                    "a": 0,
                                    "k": {"i": [[0, 0], [0, 0]], "o": [[0, 0], [0, 0]], "v": [[-278, 274], [272, 284]], "c": False},
                                    "ix": 2
                                },
                                "nm": "Path 1",
                                "mn": "ADBE Vector Shape - Group",
                                "hd": False
                            },
                            {
                                "ty": "st",
                                "c": {"a": 0, "k": [0, 0, 0, 1], "ix": 3},
                                "o": {"a": 0, "k": 100, "ix": 4},
                                "w": {"a": 0, "k": 8, "ix": 5},
                                "lc": 2,
                                "lj": 1,
                                "ml": 4,
                                "bm": 0,
                                "nm": "Stroke 1",
                                "mn": "ADBE Vector Graphic - Stroke",
                                "hd": False
                            },
                            {
                                "ty": "tr",
                                "p": {"a": 0, "k": [0, 10], "ix": 2},
                                "a": {"a": 0, "k": [0, 0], "ix": 1},
                                "s": {"a": 0, "k": [100, 100], "ix": 3},
                                "r": {"a": 0, "k": 0, "ix": 6},
                                "o": {"a": 0, "k": 100, "ix": 7},
                                "sk": {"a": 0, "k": 0, "ix": 4},
                                "sa": {"a": 0, "k": 0, "ix": 5},
                                "nm": "Transform"
                            }
                        ],
                        "nm": "Shape 1",
                        "np": 3,
                        "cix": 2,
                        "bm": 0,
                        "ix": 1,
                        "mn": "ADBE Vector Group",
                        "hd": False
                    }
                ],
                "ip": 0,
                "op": 150.000006109625,
                "st": 0,
                "ct": 1,
                "bm": 0
            }
        ],
        "markers": []
    }
    st_lottie(animacion, speed=1, width=100, height=100)

def extraer_ubicaciones(plan):
    """
    Extrae las ubicaciones del plan generado por GPT.
    Las coordenadas están en un formato interno: [COORDENADAS: latitud, longitud].
    """
    ubicaciones = []
    lineas = plan.split("\n")
    for linea in lineas:
        # Buscar el formato interno de coordenadas
        match = re.search(r"\[COORDENADAS:\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\]", linea)
        if match:
            lat = float(match.group(1))
            lon = float(match.group(2))
            # Validar coordenadas
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                # Extraer el nombre del lugar (todo antes de las coordenadas)
                nombre = re.sub(r"\s*\[COORDENADAS:.*\]", "", linea).strip()
                ubicaciones.append({"nombre": nombre, "lat": lat, "lon": lon})
            else:
                print(f"⚠️ Coordenadas inválidas: {lat}, {lon}")
    return ubicaciones

def mostrar_mapa(ubicaciones):
    """
    Muestra un mapa con las ubicaciones recomendadas.
    """
    if not ubicaciones:
        st.warning("⚠️ No se encontraron ubicaciones en el plan.")
        return

    # Crear un mapa centrado en la primera ubicación
    mapa = folium.Map(location=[ubicaciones[0]["lat"], ubicaciones[0]["lon"]], zoom_start=13, tiles="OpenStreetMap")

    # Añadir marcadores para cada ubicación
    for ubicacion in ubicaciones:
        folium.Marker(
            location=[ubicacion["lat"], ubicacion["lon"]],
            popup=ubicacion["nombre"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(mapa)

    # Mostrar el mapa en Streamlit
    folium_static(mapa)

def mostrar_plan_adaptado():
    """
    Muestra la interfaz para generar un plan adaptado al usuario.
    """
    # Mostrar título con animación Lottie
    col1, col2 = st.columns([1, 5])  # Divide la fila en dos columnas
    with col1:
        mostrar_animacion_lottie()  # Mostrar la animación Lottie
    with col2:
        st.title("Plan Adaptado a Ti")  # Título sin el emoji de ubicación

    # Obtener la API Key de OpenAI desde secrets.toml
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # Se comenta para usar en Google Cloud, donde no se pueden usar secrets con nuestro usuario
    # openai_api_key = st.secrets["OPENAI_API_KEY"]

    # Instanciar el modelo GPT
    modelo_gpt = ModeloGPT("GPT-4", "v1.0", openai_api_key)
    generador = GeneradorTextos()
    generador.agregar_modelo(modelo_gpt)

    # Obtener la ubicación y la hora configuradas por el usuario
    ubicacion = obtener_ubicacion()
    hora_local = obtener_hora_local()

    # Mostrar la ubicación y la hora actual
    st.write(f"📍 Ubicación actual: {ubicacion['ciudad']}, {ubicacion['pais']}")
    st.write(f"🕒 Hora actual: {hora_local}")

    # Entradas del usuario
    actividad = st.text_input("✍️ ¿Qué te gustaría hacer hoy? (Ejemplo: 'Quiero explorar museos')")
    estado_emocional = st.text_input("😊 ¿Cómo te sientes? (Ejemplo: 'Feliz', 'Cansado', 'Emocionado')")
    nivel_energia = st.selectbox("⚡ Nivel de energía", ["Bajo", "Medio", "Alto"])

    if st.button("Generar Plan"):
        if not actividad or not estado_emocional:
            st.error("❌ Por favor, ingresa una actividad y tu estado emocional.")
        else:
            try:
                # Convertir los datos del usuario a JSON
                datos_usuario = json.dumps({
                    "actividad": actividad,
                    "estado_emocional": estado_emocional,
                    "nivel_energia": nivel_energia.lower(),
                    "ubicacion": ubicacion,
                    "hora_local": hora_local
                })

                # Procesar la petición y generar el plan
                peticion_enriquecida = procesar_peticion(datos_usuario)
                resultado = generador.generar(peticion_enriquecida)

                if resultado and not resultado.startswith("❌"):
                    st.success("✅ Plan generado con éxito:")

                    # Eliminar las coordenadas del texto que se muestra al usuario
                    plan_sin_coordenadas = re.sub(r"\s*\[COORDENADAS:.*\]", "", resultado)

                    # Mostrar el plan completo usando st.markdown
                    st.markdown(f"**Plan de viaje:**\n{plan_sin_coordenadas}")

                    # Extraer ubicaciones del plan
                    ubicaciones = extraer_ubicaciones(resultado)
                    if ubicaciones:
                        mostrar_mapa(ubicaciones)
                    else:
                        st.warning("⚠️ No se encontraron ubicaciones en el plan.")
                else:
                    st.error("❌ Error al generar el plan. Detalles: " + resultado)

            except Exception as e:
                st.error(f"❌ Error inesperado: {str(e)}")