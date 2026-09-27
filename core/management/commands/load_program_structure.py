"""Load the Program Structure section content into the database.

This is the site's real content (the five focus areas PADEV works in), loaded
once into the live database and then maintained through the Django admin.

It is safe to run repeatedly:
  * cards that are missing are created,
  * cards that already exist are left alone, so nothing an editor has written
    is overwritten (use --force to replace their text deliberately),
  * the fallback "seed" cards from seed_data.py are deactivated, not deleted.

Usage:
    python manage.py load_program_structure
    python manage.py load_program_structure --force
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import ProgramStructure, SiteSetting


SECTION_HEADING = 'Program Structure'
SECTION_INTRO = (
    'Driven by specialized expertise, Partners in Development delivers impactful '
    'solutions across four core areas: Forest Governance, Livelihood & Enterprise '
    'Development, Strategic Communication, and Stakeholder Engagement.'
)

# Fallback cards created by seed_data.py — superseded by the real content below.
FALLBACK_SLUGS = (
    'community-forest-governance',
    'conservation-education',
    'livelihood-enterprise',
    'gender-social-inclusion',
)

CARDS = [
    {
        'title': 'Forest Governance',
        'icon_class': 'ri-tree-line',
        'theme': 'green',
        'order': 1,
        'description': (
            'Capacity building, training and policy support that establish and '
            'strengthen community forest governance institutions.'
        ),
        'detail_content': """Programs designed in the area of Forest Governance cover:

- Capacity building activities that facilitate the establishment of forest governance institutions
- A support system that strengthens the institutional capacity of forest governance structures
- Training workshops contextually designed to improve the institutional framework of forest governance bodies
- Structured activity that supports forest dependent communities to complete the legal requirements for communities to legitimize their community forest status
- Activity that Enhances coordination and policy alignment between forest governance institutions and local authorities
- Cross cutting activity that integrates the practice of gender and social inclusion in project and program design

For the last ten years, PADEV has consistently assisted the Forestry Development Authority (FDA) to model a forest governance system that ensures compliance with the framework of community-based natural resource management

To support communities to acquire the legal requirements that qualify them to attain Authorized Forest Community (AFC), PADEV introduced the Community Forest Organizing Committee (CFOC). This approach devolves greater responsibilities to local communities to go through the Nine-Step process. Adopted by FDA; this arrangement deters elite influence in the acquisition of AFC and allows forest fringe communities to navigate and appreciate the value in traversing the Nine-Step process without elite interference and influence. PADEV was the first to pilot and support communal forest governance institutions in communities at the peripheries of the Sapo National Park (SNP).

When we set build governance bodies, we improve their institutional capacity, serve as their mentor and provide them foundational knowledge to manage their groups in a more responsible and systematic manner.

Members of our team who lead forest governance activities are adept in the laws, policies and regulatory framework that guide sustainable forest management (SFM), biodiversity conservation, forest governance and climate change. The cadre of staff at PADEV made meaningful contribution to the development of the Community Rights Law (CRL) of 2009 with Respect to Forestland, led efforts to pilot it and actively participated in national and regional consultations which led to the development of the regulation to the law.""",
    },
    {
        'title': 'Livelihood & Enterprise Development',
        'icon_class': 'ri-money-dollar-circle-line',
        'theme': 'gold',
        'order': 2,
        'description': (
            'Biodiversity-compatible farming, beekeeping, savings groups and small '
            'enterprise that raise incomes for forest-fringed communities.'
        ),
        'detail_content': """Our Livelihood & Enterprise Development programs are premised on principles that reduce threat to biodiversity, mitigate climate change and minimize deforestation. Activities under our Livelihood & Enterprise Development program focus on biodiversity compatible programs including:

- Regenerative Climate-Smart Agriculture (CSA)
- Village Saving and Loan Association (VSLA)
- Beekeeping and honey production
- Small-Scale Business Development
- Handicraft production
- Sustainable production and trade in nontimber forest products (NTFPs)

Our Livelihood & Enterprise Development program provides onsite capacity building support rooted in integrative skills that promotes sustainable forest management and the long-term sustainability of the community empowerment programs we offer. When we introduce livelihood programs, we train beneficiaries and ensure that they learn the requisite skill to independently replicate the knowledge, take ownership of the process.

Since our inception, we have supported over 500 farmers by providing high-quality crop inputs. Our beneficiaries receive premium hybrid cocoa seedlings, as well as local cowpea, hot pepper, and plantain varieties to boost their production.

In 2023, we introduced seed gardens across project sites in farming communities in the Southeast of Liberia. Targeted counties included Grand Gedeh, Rivergee, Rivercess and Grand Kru. This effort gave farmers enhanced access to planting materials and reduced their reliance on imported seeds for crop production.

Our green enterprise program focuses on beekeeping, an initiative that promotes biodiversity, strengthens forest ecosystems, and uplifts the socioeconomic well-being of local communities.

Our VSLA program model enhances the security of community-managed savings, provides a sustainable informal financial alternative, enables flexible access to small loans, promotes local entrepreneurship, and serves as a financial safety net for vulnerable households and small businesses.

Our aquaculture expertise is rooted in a business-like approach that builds both the technical and entrepreneurial capacity of fish farmers. By leveraging extension services, we stimulate local growth and create direct, sustainable pathways to commercial markets.""",
    },
    {
        'title': 'Strategic Communications',
        'icon_class': 'ri-megaphone-line',
        'theme': 'navy',
        'order': 3,
        'description': (
            'Development communication and social behaviour change programming that '
            'carries project messages to the audiences who need them.'
        ),
        'detail_content': """Our strategic communication program integrates the principle of development communication. It encompasses concepts used in Social Behavior Change Communication (SBCC) to reach our target audiences. Services we deliver are designed with the understanding that communication plays a pivotal role in development and project implementation.

The success of our communication program is based on:

- The outcome of a matrix for change exercise which helps us to understand the local context, define measurable goals, determine cultural alignment, select audience types and inform planning of our communication activities
- Stakeholders input to communication products we design
- Capacity building program for community youth, young women, and local leaders who are often equipped with the needed logistics to lead awareness activities in their communities

When we implement long term projects:

- We build local structures and improve their capacity to exercise communication stewardship in their communities
- We design feedback mechanism, evaluate the impact of our communication program and adjust were applicable
- Develop communication strategy and policy to guide project communication activities""",
    },
    {
        'title': 'Stakeholder Engagement',
        'icon_class': 'ri-team-line',
        'theme': 'rose',
        'order': 4,
        'description': (
            'Consultation, coordination and collaboration that connect partners with '
            'stakeholders at landscape, subnational and national levels.'
        ),
        'detail_content': """We believe that successful Community-Based Natural Resource Management (CBNRM) depends on effective stakeholder engagement. This entails the active participation of everyone who shares an interest in local forest and community resources.

Guided by the principles of consultation, coordination, and collaboration, we align our stakeholder engagement activity across three critical levels:

- Landscape
- Subnational
- National

Our stakeholder engagement program bridges critical communication gaps, seamlessly connecting development partners and donor organizations with essential on-the-ground stakeholders at every level.

The seamless integration of our technical and logistical capabilities eliminates the complexity of contracting separate institutions. By providing both services under one roof, we streamline operations and offer stakeholders a single, unified point of contact.""",
    },
    {
        'title': 'Training and Facilitation',
        'icon_class': 'ri-graduation-cap-line',
        'theme': 'green',
        'order': 5,
        'description': (
            'Expert facilitation using Advanced Participatory Methods, including the '
            'national Community Forestry Working Group platform.'
        ),
        'detail_content': """Our team consists of highly skilled trainers with proven expertise in group facilitation. This strength is grounded in their advanced mastery of Advanced Participatory Methods (APM), acquired through an intensive facilitation program sponsored by Tetra Tech. Demonstrating this expertise at the highest level, PADEV leads the facilitation for the Community Forestry Working Group (CFWG)—the single largest national platform in Liberia dedicated to community forestry policy and practice.""",
    },
]


class Command(BaseCommand):
    help = 'Load the Program Structure cards (the five focus areas) into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Overwrite the title, text, icon and theme of cards that already exist.',
        )

    def handle(self, *args, **options):
        force = options['force']
        created = updated = skipped = 0

        # 1. Section heading + introduction (only if they were cleared)
        site = SiteSetting.get_instance()
        if not site.program_structure_heading:
            site.program_structure_heading = SECTION_HEADING
            site.save()
            self.stdout.write('  filled in the section heading')
        if not site.program_structure_intro:
            site.program_structure_intro = SECTION_INTRO
            site.save()
            self.stdout.write('  filled in the section introduction')

        # 2. The five cards
        for data in CARDS:
            slug = slugify(data['title'])
            card = ProgramStructure.objects.filter(slug=slug).first()

            if card is None:
                ProgramStructure.objects.create(slug=slug, **data)
                created += 1
                self.stdout.write(self.style.SUCCESS('  created  %s' % data['title']))
                continue

            if force:
                for field, value in data.items():
                    setattr(card, field, value)
                card.slug = slug
                card.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS('  updated  %s' % data['title']))
            elif not card.detail_content:
                card.detail_content = data['detail_content']
                card.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS('  filled in the article for %s' % data['title']))
            else:
                skipped += 1
                self.stdout.write('  kept     %s (already has content)' % data['title'])

        # 3. Retire the fallback seed cards (deactivated, never deleted)
        retired = ProgramStructure.objects.filter(
            slug__in=FALLBACK_SLUGS, is_active=True,
        ).update(is_active=False)
        if retired:
            self.stdout.write(self.style.WARNING('  deactivated %d fallback seed card(s)' % retired))

        self.stdout.write(self.style.SUCCESS(
            'Program Structure ready: %d created, %d updated, %d left as-is, %d retired.'
            % (created, updated, skipped, retired)
        ))
