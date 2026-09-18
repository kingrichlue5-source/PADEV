from django.core.management.base import BaseCommand
from datetime import date
from core.models import (
    Program, Project, NewsUpdate, SuccessStory, TeamMember, Client,
    Publication, ProcurementOpportunity, Career,
    SiteSetting, NavigationMenu, HeroSlide,
)

CONTENT_MODELS = [
    Program, Project, NewsUpdate, SuccessStory, TeamMember, Client,
    Publication, ProcurementOpportunity, Career,
    NavigationMenu, HeroSlide,
]


class Command(BaseCommand):
    help = 'Seeds PADEV (Partners in Development) portal content'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing existing demo content...'))
        for model in CONTENT_MODELS:
            model.objects.all().delete()

        # ─── CMS Site Settings (Singleton) ───
        site_settings = SiteSetting.get_instance()
        site_settings.site_name = 'Partners in Development (PADEV)'
        site_settings.agency_acronym = 'PADEV'
        site_settings.logo = 'site/padev-logo.png'
        site_settings.contact_email = 'info@padev.org'
        site_settings.contact_phone = '+231 088 651 8396'
        site_settings.address = 'Sophie Community, Opposite HILA School, Congo Town, Liberia'
        site_settings.social_links = {
            'facebook': 'https://web.facebook.com/PADEVLIBERIA',
            'instagram': 'https://www.instagram.com/padevliberia/',
        }
        site_settings.save()

        # ─── Navigation Menus ───
        nav_defs = [
            ('Home', '/', 1),
            ('About Us', '/#about', 2),
            ('Our Team', '/team/', 3),
            ('Programmes', '/programmes/', 4),
            ('Projects', '/projects/', 5),
            ('Publications', '/publications/', 6),
            ('Contact Us', '/contact/', 7),
        ]
        for title, url, order in nav_defs:
            NavigationMenu.objects.get_or_create(
                title=title,
                defaults={'url': url, 'order': order, 'is_active': True},
            )

        # ─── Hero Slides ───
        HeroSlide.objects.get_or_create(
            title='Building Alliances to Mitigate Global Environmental Challenges',
            defaults={
                'badge_text': 'Community-Based Natural Resource Management',
                'description': 'PADEV supports community-based natural resource management and sustainable forest conservation across Liberia, empowering forest-fringed communities through governance, livelihoods, and environmental education.',
                'slide_image': 'hero/hero-tgks-forest.jpg',
                'primary_cta_text': 'Explore Our Work',
                'primary_cta_url': '/projects/',
                'secondary_cta_text': 'About PADEV',
                'secondary_cta_url': '/#about',
                'order': 1,
                'is_active': True,
            },
        )
        HeroSlide.objects.get_or_create(
            title='Protecting the Sapo National Park & Liberia’s Forests',
            defaults={
                'badge_text': 'Conservation in Action',
                'description': 'From the Tai-Grebo-Krahn-Sapo Transboundary Forest Landscape to community outreach structures, PADEV works hand-in-hand with communities to protect biodiversity hotspots.',
                'slide_image': 'hero/hero-sapo-park.jpg',
                'primary_cta_text': 'View Projects',
                'primary_cta_url': '/projects/',
                'secondary_cta_text': 'Contact Us',
                'secondary_cta_url': '/contact/',
                'order': 2,
                'is_active': True,
            },
        )
        HeroSlide.objects.get_or_create(
            title='People, Forests & Livelihoods — Together',
            defaults={
                'badge_text': 'Established 2016',
                'description': 'Founded in August 2016, PADEV builds on the collective competence of experienced professionals to deliver community development and natural resource management across over 100 forest-fringed communities.',
                'slide_image': 'hero/hero-elephants.jpg',
                'primary_cta_text': 'Our Programmes',
                'primary_cta_url': '/programmes/',
                'secondary_cta_text': 'About PADEV',
                'secondary_cta_url': '/#about',
                'order': 3,
                'is_active': True,
            },
        )

        # ─── Programs ───
        prog_cbnrm, _ = Program.objects.get_or_create(
            title='Community-Based Natural Resource Management (CBNRM)',
            defaults={
                'icon_class': 'ri-tree-line',
                'short_description': 'Supporting forest-fringed communities to govern and manage communal forests and natural resources through participatory, community-based structures.',
                'description': 'PADEV is a leading national institution that builds its intervention on the collective competence of its diverse professionals. Our cadre of staff is one of the most experienced in community-based natural resource management (CBNRM) in Liberia. Through a participatory approach and building on existing frameworks, we work with the Forestry Development Authority (FDA) and local community leaders to facilitate the formation of forest resource governance structures that man protected areas and manage communal forest landscapes.',
                'cover_image': 'programs/cbnrm.jpg',
                'status': 'active',
                'county': 'national',
                'budget': '',
                'target_beneficiaries': '100+ Forest-Fringed Communities',
                'is_featured': True,
            },
        )

        prog_forest, _ = Program.objects.get_or_create(
            title='Forest Governance & Conservation',
            defaults={
                'icon_class': 'ri-plant-line',
                'short_description': 'Establishing and strengthening community forest governance entities and supporting protected area management in Liberia.',
                'description': 'Under the Liberia Forest Sector Project (LFSP) and the Tai-Grebo-Krahn-Sapo (TGKS) Transboundary Forest Landscape project, PADEV facilitated the establishment of functional forest governance entities, raised awareness on the Community Rights Law (CRL) with Respect to Forestland, and supported the establishment of the initial Authorized Forest Communities (AFC). In recognition of its influence and support to the environmental sector, PADEV holds formal sector clearances from the Environmental Protection Agency (EPA) and the Ministry of Agriculture (MOA).',
                'cover_image': 'programs/forest-governance.jpg',
                'status': 'active',
                'county': 'national',
                'budget': '',
                'target_beneficiaries': '27 Communities in 6 Counties',
                'is_featured': True,
            },
        )

        prog_livelihood, _ = Program.objects.get_or_create(
            title='Livelihood & Enterprise Development',
            defaults={
                'icon_class': 'ri-seedling-line',
                'short_description': 'Bridging gaps in food security and income disparity through conservation agriculture, beekeeping, and community enterprise development groups.',
                'description': 'PADEV brings forest-fringed community men and women to the forefront of conservation agriculture, helping them raise income from pepper cultivated on small plots. Community groups were trained on beekeeping with about 190 beehives set up across 10 sites, over 80% of which are thriving. Consignments of agricultural inputs were supplied to underserved and hard-to-reach communities, and enterprise development groups were established to sustain incomes beyond project cycles.',
                'cover_image': 'programs/livelihood.jpg',
                'status': 'active',
                'county': 'national',
                'budget': '',
                'target_beneficiaries': '190 Beehives, 10 Sites',
                'is_featured': True,
            },
        )

        prog_sbcc, _ = Program.objects.get_or_create(
            title='Social Behavior Change Communication & Environmental Education',
            defaults={
                'icon_class': 'ri-megaphone-line',
                'short_description': 'Community outreach and environmental education delivered through a matrix for change communication process.',
                'description': 'Through a matrix for change communication process, our team works with various audience types at the district and community levels whose input is incorporated in key communication messages. We inspire pupils in primary community schools through environmental clubs to gain their empathy for biodiversity conservation, train school administrators based on a USAID PROSPER-funded environmental education curriculum, and build community theater troupes to lead conservation outreach in the constituents of their communities.',
                'cover_image': 'programs/sbcc.jpg',
                'status': 'active',
                'county': 'national',
                'budget': '',
                'target_beneficiaries': '20+ Community Schools',
                'is_featured': True,
            },
        )

        # ─── Projects ───
        Project.objects.get_or_create(
            title='Tai-Grebo-Krahn-Sapo (TGKS) Transboundary Forest Landscape',
            defaults={
                'program': prog_forest,
                'short_description': 'Collaboratively implemented with USAID under the West Africa Biodiversity and Climate Change (WA BiCC) program from 2018 to 2020.',
                'description': 'PADEV collaboratively implemented the Tai-Grebo-Krahn-Sapo Transboundary Forest Landscape (TGKS) project, funded by USAID under the West Africa Biodiversity and Climate Change (WA BiCC) program. As a sub-grantee to Fauna & Flora International (FFI), PADEV led and facilitated the establishment of nine (9) functional forest governance entities, built capacities in over 70 park-fringed communities around the Sapo National Park (SNP) through livelihood support programs, established enterprise development groups, introduced and operationalized environmental education programs in over 20 schools, and set up and strengthened community conservation education and awareness bodies.',
                'cover_image': 'projects/tgks.jpg',
                'status': 'completed',
                'county': 'national',
                'location_details': 'Sinoe, Grand Gedeh & River Gee counties',
                'progress_percentage': 100,
                'budget': '',
                'contractor': 'USAID (WA BiCC) / Fauna & Flora International (FFI)',
                'start_date': date(2018, 1, 1),
                'completion_date': date(2020, 12, 31),
                'is_featured': True,
            },
        )

        Project.objects.get_or_create(
            title='Liberia Forest Sector Project (LFSP) — Community Forest Governance',
            defaults={
                'program': prog_forest,
                'short_description': 'Consulting services for awareness raising and the establishment of community forest governance entities in over 27 communities across six counties.',
                'description': 'From 2019 to 2021, PADEV successfully completed a consulting services contract awarded by the Forestry Development Authority (FDA) under the Liberia Forest Sector Project (LFSP) for Awareness Raising and Support for the Establishment of Community Forest Governance Entities in over 27 communities in six (6) counties. PADEV, in consultation with FDA, developed and disseminated illustrative materials including the broadcast of radio programs, and hosted several public events bringing together scores of local and public officials. The project was a World Bank-managed project funded by the Government of Norway.',
                'cover_image': 'projects/lfsp.jpg',
                'status': 'completed',
                'county': 'national',
                'location_details': 'Six counties across Liberia',
                'progress_percentage': 100,
                'budget': '',
                'contractor': 'Forestry Development Authority (FDA) / World Bank',
                'start_date': date(2019, 1, 1),
                'completion_date': date(2021, 12, 31),
                'is_featured': True,
            },
        )

        Project.objects.get_or_create(
            title='Sapo National Park Community Conservation Program',
            defaults={
                'program': prog_cbnrm,
                'short_description': 'Empowering 70+ park-fringed communities through governance, livelihoods, and conservation awareness around Liberia’s largest protected area.',
                'description': 'Sapo National Park is the largest conservation area in Liberia, measuring over 180,000 hectares and stretching across Sinoe, Grand Gedeh and River Gee. PADEV works in collaboration with the Forestry Development Authority (FDA) and Fauna & Flora International (FFI) to roll out communication activities throughout the landscape, facilitate the formation of community based outreach structures, and support the protection and management of the Park. Community entities are propping the FDA to take care of the Sapo Park.',
                'cover_image': 'projects/sapo-community.jpg',
                'status': 'completed',
                'county': 'sinoe',
                'location_details': 'Sapo National Park (Jalay Town & Nyennawliaken)',
                'progress_percentage': 100,
                'budget': '',
                'contractor': 'Fauna & Flora International (FFI) / FDA',
                'start_date': date(2018, 6, 1),
                'completion_date': date(2021, 12, 31),
                'is_featured': True,
            },
        )

        Project.objects.get_or_create(
            title='Conservation Agriculture & Beekeeping Enterprise',
            defaults={
                'program': prog_livelihood,
                'short_description': 'Conservation agriculture and beekeeping enterprises that raise incomes for forest-fringed communities.',
                'description': 'PADEV/FFI brought forest-fringed community men and women to the forefront of conservation agriculture and helped them raise hefty income from pepper cultivated on small plots through a pilot project. Underserved and hard-to-reach communities were supplied consignments of agricultural inputs and trained. As part of the community conservation enterprise, community groups were trained on beekeeping; about 190 beehives were set up across 10 sites and over 80% are thriving.',
                'cover_image': 'projects/agri-beekeeping.jpg',
                'status': 'completed',
                'county': 'grand_gedeh',
                'location_details': 'Nyennawliaken & surrounding communities',
                'progress_percentage': 100,
                'budget': '',
                'contractor': 'Fauna & Flora International (FFI)',
                'start_date': date(2019, 1, 1),
                'completion_date': date(2021, 12, 31),
                'is_featured': True,
            },
        )

        Project.objects.get_or_create(
            title='Community Theater Troupes for Conservation Outreach',
            defaults={
                'program': prog_sbcc,
                'short_description': 'Formation and capacity building of two community theater troupes to lead conservation awareness around the Sapo National Park.',
                'description': 'In late 2019, the PADEV and FFI team facilitated the formation of two theater troupes in the landscape, made up predominantly of young men and women who are future beneficiaries of their forest resources. The troupes lead conservation awareness activities in the constituents of the Park and assume greater responsibility for its protection and management. In early 2020, both troupes were formally handed over to their respective local authorities — one at Jalay Town, the headquarters of the Park, and the other at Nyennawliaken in the east. Two years following the end of the TGKS project, the troupes still exist and have been integrated into the social structure of their communities.',
                'cover_image': 'projects/theater-troupes.jpg',
                'status': 'completed',
                'county': 'grand_gedeh',
                'location_details': 'Jalay Town & Nyennawliaken',
                'progress_percentage': 100,
                'budget': '',
                'contractor': 'Fauna & Flora International (FFI)',
                'start_date': date(2019, 10, 1),
                'completion_date': date(2021, 12, 31),
                'is_featured': False,
            },
        )

        # ─── News & Updates ───
        news1, _ = NewsUpdate.objects.get_or_create(
            title='To Strengthen Capacity in Forest Conservation, PADEV Trains Field Extension Staff',
            defaults={
                'author': 'PADEV Communications Team',
                'category': 'field_update',
                'excerpt': 'PADEV successfully completed a weeklong in-house training for eight field extension staff focused on Participatory Rural Appraisal, Gender and Social Inclusion, biodiversity conservation, conservation communication, and GIS/GPS operation.',
                'content': 'Monrovia — Partners in Development (PADEV), a national environmental organization, has successfully completed a weeklong in-house training for eight (8) of its field extension staff. The training essentially focused on the fundamentals of Participatory Rural Appraisal (PRA), Gender and Social Inclusion (GESI), Biodiversity Conservation, Conservation Communication as well as Geo-Information Services (GIS) and Global Positioning System (GPS) operation. The principal objective of the training was to improve the technical capacity of the organization’s staff; build and prepare a resilient team of reliable front liners to support the implementation of work related to biodiversity conservation and ensure the delivery of quality services at the project level. The training was hosted in the conference facility of Wild Chimpanzee Foundation (WCF) in Congo Town, and it ran from October 5 through the 13th. The lead facilitator was Dr. Samuel N. Koffa, an independent consultant and scientist with extensive experience in the forest sector of Liberia. Speaking to participants at the opening of the weeklong exercise, PADEV Team Leader, Nobeh, Jackson underscored the significance of strengthening the technical capacity of the field staff.',
                'featured_image': 'news/padev-training.jpg',
                'is_featured': True,
            },
        )
        NewsUpdate.objects.filter(pk=news1.pk).update(published_date=date(2021, 10, 18))

        news2, _ = NewsUpdate.objects.get_or_create(
            title='PADEV Builds and Strengthens the Capacity of Community Based Outreach Structures',
            defaults={
                'author': 'PADEV Communications Team',
                'category': 'field_update',
                'excerpt': 'Sapo National Park is the largest conservation area in Liberia, spanning over 180,000 hectares across Sinoe, Grand Gedeh and River Gee. PADEV facilitated the formation of two community theater troupes to lead conservation awareness in the Park’s constituents.',
                'content': 'Sapo National Park is currently the largest conservation area in Liberia. It measures over 180,000 hectares and stretches across three of Liberia’s southeastern counties of Sinoe, Grand Gedeh and River Gee. Upon the inception of the USAID WA BiCC funded Tai-Grebo-Krahn-Sapo (TGKS) Transboundary Boundary project, PADEV in collaboration with FFI identified the lack of effective awareness and community sensitization as one of the major drawbacks to the protection of the Park. In late 2019, the team successfully facilitated the formation of two theater troupes in the landscape. Made up predominantly of young men and women, the roles of the troupes are to lead conservation awareness activities in the constituents of the Park and to assume greater responsibility of its protection and management. In early 2020, both troupes were formally handed over to their respective local authorities — one situated westward in Jalay Town, the headquarters of the Park, and the other located in the east at Nyennawliaken. Two years following the end of the TGKS project, the troupes still exist and have been integrated in the social structure of their communities.',
                'featured_image': 'news/outreach-structures.jpg',
                'is_featured': True,
            },
        )
        NewsUpdate.objects.filter(pk=news2.pk).update(published_date=date(2020, 3, 1))

        news3, _ = NewsUpdate.objects.get_or_create(
            title='The Case of Endangered Elephants in the Sapo National Park',
            defaults={
                'author': 'PADEV Field Operations Unit',
                'category': 'field_update',
                'excerpt': 'In March 2019, PADEV Field Extension staff uncovered the decomposed carcasses of two of four elephants killed by a poacher in the Sapo National Park.',
                'content': 'In March 2019, PADEV Field Extension staff working through conservation forest governance groups uncovered the decomposed carcasses of two (2) of four (4) elephants killed by a poacher in the Sapo National Park (SNP). With the support of the PADEV/FFI field team, the matter was reported to the Forestry Development Authority (FDA) and the poacher was prosecuted.',
                'featured_image': 'news/elephants.jpg',
                'is_featured': False,
            },
        )
        NewsUpdate.objects.filter(pk=news3.pk).update(published_date=date(2019, 3, 31))

        # ─── Success Stories ───
        SuccessStory.objects.get_or_create(
            title='Eco-Champions: Women Leading Conservation Outreach',
            defaults={
                'beneficiary_name': 'Eco-Champions Women’s Group (Sinoe County)',
                'county': 'sinoe',
                'quote': 'The group of twenty women made outstanding contributions to conservation awareness, having covered over 70 park-fringed communities before the end of the USAID WA BiCC project.',
                'content': 'When we work with communities, we place a lot of emphasis on the inclusion of marginalized people including women, boys, and girls. In 2018, PADEV supported the formation of a women’s group to support conservation outreach in communities around the Sapo National Park. Referred to as Eco-champions, the group of twenty women made outstanding contributions to conservation awareness, having covered over 70 park-fringed communities before the end of the USAID WA BiCC project.',
                'featured_image': 'stories/eco-champions.jpg',
                'is_featured': True,
            },
        )

        SuccessStory.objects.get_or_create(
            title='Community Theater Troupes Take the Stage for Conservation',
            defaults={
                'beneficiary_name': 'Jalay Town & Nyennawliaken Theater Troupes',
                'county': 'grand_gedeh',
                'quote': 'Two years following the end of the TGKS project, the troupes still exist and have been integrated in the social structure of their communities.',
                'content': 'In late 2019, the PADEV and FFI team facilitated the formation of two theater troupes in the Sapo landscape, made up predominantly of young men and women who are future beneficiaries of their forest resources. In early 2020, both troupes were formally handed over to their respective local authorities — one at Jalay Town, the headquarters of the Park, and the other at Nyennawliaken in the east.',
                'featured_image': 'stories/theater-troupes.jpg',
                'is_featured': True,
            },
        )

        SuccessStory.objects.get_or_create(
            title='Pepper Cultivation Boosts Incomes for Forest-Fringed Communities',
            defaults={
                'beneficiary_name': 'Forest-Fringed Community Farmers',
                'county': 'grand_gedeh',
                'quote': 'PADEV/FFI brought forest-fringed community men and women to the forefront of conservation agriculture and helped them raise hefty income from pepper cultivated on small plots.',
                'content': 'Through a pilot project, underserved and hard-to-reach communities were supplied consignments of agricultural inputs and trained. Men and women farmers cultivated high-grade pepper on small plots, generating significant income and strengthening food security while reducing pressure on the forest.',
                'featured_image': 'stories/pepper.jpg',
                'is_featured': True,
            },
        )

        SuccessStory.objects.get_or_create(
            title='Beekeeping Thrives Across the Sapo Landscape',
            defaults={
                'beneficiary_name': 'Community Conservation Enterprise Groups',
                'county': 'sinoe',
                'quote': 'About 190 beehives were set up across 10 sites and over 80% are thriving.',
                'content': 'As part of the community conservation enterprise, community groups were trained on beekeeping. About 190 beehives were set up across 10 sites in the Sapo landscape, and more than 80 percent are thriving — generating honey income for forest-fringed communities while promoting conservation.',
                'featured_image': 'stories/beekeeping.jpg',
                'is_featured': True,
            },
        )

        # ─── Team Members ───
        team_defs = [
            {
                'full_name': 'Jackson S. Nobeh',
                'position': 'Principal Founder & Team Leader',
                'role_category': 'management',
                'photo': 'team/jackson-nobeh.png',
                'order': 1,
                'bio': 'Jackson S. Nobeh is the principal founder of PADEV and the first head of its management. With extensive experience in community-based natural resource management (CBNRM) in Liberia, he previously worked with the USAID funded Land Rights and Community Forestry Program (LRCFP) and USAID PROSPER, where he played a leading role in developing practical, replicable models to guide and administer community forestry in Liberia. He led PADEV’s implementation of the USAID WA BiCC funded TGKS Transboundary Forest Landscape project and the FDA/LFSP community forest governance project.',
            },
            {
                'full_name': 'Martin A. T. Vesselee',
                'position': 'Cofounder & Deputy Team Leader',
                'role_category': 'management',
                'photo': 'team/martin-vesselee.png',
                'order': 2,
                'bio': 'Martin A. T. Vesselee is a cofounder of PADEV and serves as Deputy Team Leader. A member of PADEV’s management team with a background in forestry and development communication, he supports the day-to-day leadership of the organization’s community-based natural resource management and forest governance programs across Liberia.',
            },
            {
                'full_name': 'Fred Johnson',
                'position': 'Logistics Officer',
                'role_category': 'management',
                'photo': 'team/fred-johnson.png',
                'order': 3,
                'bio': 'Fred Johnson is PADEV’s Logistics Officer. He ensures the efficient planning, procurement, and delivery of field operations — moving teams, equipment, and supplies to support conservation and community development activities in hard-to-reach forest-fringed communities.',
            },
            {
                'full_name': 'Gibson Z. Maximore',
                'position': 'Administrative Officer',
                'role_category': 'management',
                'photo': 'team/gibson-maximore.png',
                'order': 4,
                'bio': 'Gibson Z. Maximore is PADEV’s Administrative Officer. He manages the organization’s administrative systems, human resources, and office operations, keeping the institution accountable and transparent in its service delivery.',
            },
            {
                'full_name': 'Levato Akoi-Forkpa',
                'position': 'Livelihood & Enterprise Development Specialist',
                'role_category': 'management',
                'photo': 'team/levato-akoi-forkpa.png',
                'order': 5,
                'bio': 'Levato Akoi-Forkpa is PADEV’s Livelihood and Enterprise Development Specialist. She brings forest-fringed community men and women to the forefront of conservation agriculture and beekeeping enterprise, helping them raise incomes from pepper cultivation, beehives, and community enterprise groups that bridge gaps in food security and income disparity.',
            },
            {
                'full_name': 'Eugene P. S. Gibson',
                'position': 'Snr. Field Coordinator — M&E',
                'role_category': 'management',
                'photo': 'team/eugene-gibson.png',
                'order': 6,
                'bio': 'Eugene P. S. Gibson is PADEV’s Senior Field Coordinator for Monitoring & Evaluation. He coordinates field teams and ensures the delivery of quality, evidence-based results across PADEV’s projects — from the Sapo National Park landscape to the Northwest of Liberia.',
            },
            {
                'full_name': 'Ousman F. Feika',
                'position': 'Cofounder (Resigned)',
                'role_category': 'founder',
                'photo': 'team/ousman-feika.png',
                'order': 1,
                'bio': 'Ousman F. Feika was a cofounder of PADEV and a member of its initial management team. He contributed to the founding vision of a national institution building alliances to mitigate global environmental challenges.',
            },
            {
                'full_name': 'Joshua M. Williams',
                'position': 'Cofounder & Board Member',
                'role_category': 'founder',
                'photo': 'team/joshua-williams.png',
                'order': 2,
                'bio': 'Joshua M. Williams is a cofounder of PADEV and a member of its Board of Directors. He helped establish the organization in August 2016 and continues to guide its governance and strategic direction.',
            },
            {
                'full_name': 'Dominic D. N. Kweme',
                'position': 'Cofounder',
                'role_category': 'founder',
                'photo': 'team/dominic-kweme.png',
                'order': 3,
                'bio': 'Dominic D. N. Kweme is a cofounder of PADEV. With a background in finance and economics, he supported the establishment of the institution and its early community development programming.',
            },
            {
                'full_name': 'Juah K. Feika',
                'position': 'Chairperson, Board of Directors',
                'role_category': 'board',
                'order': 1,
                'bio': 'Juah K. Feika serves as Chairperson of PADEV’s Board of Directors, providing governance and oversight to ensure the organization delivers quality, evidence-based results to its clients and communities.',
            },
            {
                'full_name': 'Rev. T. Doe Johnson',
                'position': 'Member, Board of Directors',
                'role_category': 'board',
                'order': 2,
                'bio': 'Rev. T. Doe Johnson is a member of PADEV’s Board of Directors, contributing guidance on the organization’s mission, values, and community-facing programming.',
            },
        ]
        for member in team_defs:
            TeamMember.objects.get_or_create(
                full_name=member['full_name'],
                defaults=member,
            )

        # ─── Clients & Partners ───
        client_defs = [
            {
                'name': 'USAID',
                'logo': 'clients/usaid.jpg',
                'website': 'https://www.usaid.gov/liberia',
                'order': 1,
            },
            {
                'name': 'Fauna & Flora International (FFI)',
                'logo': 'clients/ffi.png',
                'website': 'https://www.fauna-flora.org',
                'order': 2,
            },
            {
                'name': 'Forestry Development Authority (FDA)',
                'logo': 'clients/fda.png',
                'website': 'https://www.fda.gov.lr',
                'order': 3,
            },
            {
                'name': 'The World Bank',
                'logo': 'clients/world-bank.png',
                'website': 'https://www.worldbank.org',
                'order': 4,
            },
        ]
        for client in client_defs:
            Client.objects.get_or_create(
                name=client['name'],
                defaults=client,
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded PADEV content!'))
