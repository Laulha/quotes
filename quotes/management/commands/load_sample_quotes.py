from django.core.management.base import BaseCommand
from quotes.models import Quote


class Command(BaseCommand):
    help = 'Charge des citations d\'exemple dans la base de données'

    def handle(self, *args, **kwargs):
        quotes_data = [
            {
                'text': 'La vie, c\'est comme une bicyclette, il faut avancer pour ne pas perdre l\'équilibre.',
                'author': 'Albert Einstein'
            },
            {
                'text': 'Le succès n\'est pas final, l\'échec n\'est pas fatal : c\'est le courage de continuer qui compte.',
                'author': 'Winston Churchill'
            },
            {
                'text': 'L\'imagination est plus importante que le savoir.',
                'author': 'Albert Einstein'
            },
            {
                'text': 'Soyez vous-même ; tous les autres sont déjà pris.',
                'author': 'Oscar Wilde'
            },
            {
                'text': 'Deux choses sont infinies : l\'univers et la bêtise humaine. Mais en ce qui concerne l\'univers, je n\'en ai pas encore acquis la certitude absolue.',
                'author': 'Albert Einstein'
            },
            {
                'text': 'La seule façon de faire du bon travail est d\'aimer ce que vous faites.',
                'author': 'Steve Jobs'
            },
            {
                'text': 'Dans vingt ans, vous serez plus déçu par les choses que vous n\'avez pas faites que par celles que vous avez faites.',
                'author': 'Mark Twain'
            },
            {
                'text': 'Le meilleur moment pour planter un arbre était il y a 20 ans. Le deuxième meilleur moment est maintenant.',
                'author': 'Proverbe chinois'
            },
        ]

        for quote_data in quotes_data:
            Quote.objects.get_or_create(
                text=quote_data['text'],
                author=quote_data['author']
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ {len(quotes_data)} citations ont été chargées avec succès !'
            )
        )
