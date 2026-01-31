from django import template

register = template.Library()

@register.filter
def gramos_a_kg(gramos):
    """Convierte gramos a kilogramos con formato legible"""
    try:
        gramos = float(gramos)
        return f"{gramos / 1000:.2f}".rstrip('0').rstrip('.')
    except (ValueError, TypeError):
        return gramos
