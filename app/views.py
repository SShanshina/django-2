from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    response = request.GET.get('from-landing')
    print(response)
    counter_click[response] += 1
    print(f'Количество переходов: original - {counter_click["original"]}, test - {counter_click["test"]}')
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    response = request.GET.get('ab-test-arg')
    print(response)
    if response == 'original':
        counter_show[response] += 1
        print(f'Количество показов: original - {counter_show["original"]}, test - {counter_show["test"]}')
        return render(request, 'landing.html')
    elif response == 'test':
        counter_show[response] += 1
        print(f'Количество показов: original - {counter_show["original"]}, test - {counter_show["test"]}')
        return render(request, 'landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    original_result = counter_show['original'] / counter_click['original']
    print(original_result)
    test_result = counter_show['test'] / counter_click['test']
    print(test_result)
    return render(request, 'stats.html', context={
        'test_conversion': round(test_result, 2),
        'original_conversion': round(original_result, 2),
    })
