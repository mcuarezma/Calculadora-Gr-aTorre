# grua.py

class CalculadoraGrua:
    def __init__(self):
        # El momento máximo estructural ajustado para el límite industrial pedido
        self.momento_estabilidad = 120.0  # Capacidad de torque (t·m)
        self.limite_absoluto_carga = 12.0 # Tope estricto solicitado

    def calcular_estabilidad(self, peso_carga, distancia_carro, altura_izaje=0):
        # Momento generado por la carga (Fuerza x Distancia)
        momento_carga = peso_carga * distancia_carro
        
        # Capacidad límite máxima en este radio específico (Sin pasarse nunca de 12)
        carga_max_distancia = self.momento_estabilidad / distancia_carro if distancia_carro > 0 else 0
        if carga_max_distancia > self.limite_absoluto_carga:
            carga_max_distancia = self.limite_absoluto_carga
        
        # Factor de seguridad (FS = Momento Resistente / Momento Volcante)
        if momento_carga > 0:
            factor_seguridad = self.momento_estabilidad / momento_carga
        else:
            factor_seguridad = 99.9

        # Criterios de aceptación (FS mínimo de 1.2 y peso menor al permitido)
        es_seguro = factor_seguridad >= 1.2 and peso_carga <= carga_max_distancia and peso_carga <= self.limite_absoluto_carga

        if es_seguro:
            estado = "✅ OPERACIÓN SEGURA — Dentro de los límites estructurales"
        else:
            if peso_carga > self.limite_absoluto_carga:
                estado = f"❌ ALERTA: PESO EXCEDIDO — Supera la carga máxima permitida de {self.limite_absoluto_carga} Ton"
            else:
                estado = "❌ ALERTA: RIESGO DE VOLCADO — Supera el momento límite de la pluma"

        return {
            "momento_carga": momento_carga,
            "momento_estabilidad": self.momento_estabilidad,
            "factor_seguridad": factor_seguridad,
            "carga_max_distancia": carga_max_distancia,
            "es_seguro": es_seguro,
            "estado": estado
        }