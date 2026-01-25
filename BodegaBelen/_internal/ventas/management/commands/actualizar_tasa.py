from django.core.management.base import BaseCommand
from django.utils import timezone
import requests
from decimal import Decimal
from ventas.models import TasaCambio


class Command(BaseCommand):
    help = 'Actualiza la tasa de cambio desde la API del BCV'

    def handle(self, *args, **kwargs):
        try:
            # Obtener tasa desde la API
            response = requests.get('https://pydolarve.org/api/v1/dollar/page', timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Buscar la tasa del BCV
            tasa_bcv = None
            for monitor in data.get('monitors', {}).values():
                if monitor.get('title') == 'BCV':
                    tasa_bcv = monitor.get('price')
                    break
            
            if not tasa_bcv:
                self.stdout.write(self.style.WARNING('No se encontró la tasa del BCV en la respuesta'))
                return
            
            # Convertir a Decimal
            tasa_decimal = Decimal(str(tasa_bcv))
            
            # Verificar si ya existe una tasa para hoy
            hoy = timezone.now().date()
            tasa_existente = TasaCambio.objects.filter(fecha=hoy).first()
            
            if tasa_existente:
                if tasa_existente.tasa != tasa_decimal:
                    tasa_existente.tasa = tasa_decimal
                    tasa_existente.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Tasa actualizada: 1 USD = {tasa_decimal} Bs'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'La tasa ya está actualizada: 1 USD = {tasa_decimal} Bs'
                        )
                    )
            else:
                TasaCambio.objects.create(tasa=tasa_decimal, fuente='BCV - API')
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Nueva tasa creada: 1 USD = {tasa_decimal} Bs'
                    )
                )
                
        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error al obtener la tasa de cambio: {str(e)}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error inesperado: {str(e)}'
                )
            )
