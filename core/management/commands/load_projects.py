"""
Load the five project factsheets into the database.

    python manage.py load_projects
    python manage.py load_projects --force

Projects that are missing are created. Projects that already exist are left
exactly as an editor saved them unless --force is passed. Progress is derived
from the start and end dates (never above 95% while a project is still running)
and can be adjusted afterwards in the admin panel.
"""

from datetime import date

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Project


def progress_for(start, end, status):
    """Time elapsed between start and end, capped while a project is ongoing."""
    if not start or not end:
        return 0
    today = date.today()
    span = (end - start).days
    if span <= 0:
        return 100 if status == 'completed' else 95
    if today <= start:
        return 0
    if today >= end:
        return 100 if status == 'completed' else 95
    elapsed = round(((today - start).days / span) * 100)
    if status != 'completed':
        elapsed = min(elapsed, 95)
    return max(elapsed, 0)


PROJECTS = [
    {
        'title': "Guinea Forest Integrated Programs (GFIP)",
        'short_description': (
            "Protecting intact forest landscapes in Northwest Liberia and improving local "
            "livelihoods, delivered with the EPA and SCNL across Lofa, Gbarpolu and Grand "
            "Cape Mount."
        ),
        'description': (
            "**Liberia Project Title:** Strengthening Conservation and Effective Governance of "
            "Liberia's Critical Forests in the Northwest Liberia Landscape.\n\n"
            "**Project Summary**\n\n"
            "- The overarching goal of the project is to protect intact forest landscapes in "
            "Northwest Liberia, deliver vital ecosystem services, and support socioeconomic "
            "improvement for local communities.\n"
            "- PADEV leads implementation of Component 2, which focuses on the promotion of "
            "innovative climate-resilient and conservation-friendly livelihoods and enterprises.\n\n"
            "**Expected Project Outcome**\n\n"
            "- Management of land outside protected and proposed protected areas is improved, "
            "with 30,020 people (17,950 male, 12,070 female) benefiting from the project and "
            "undertaking improved land-use practices.\n\n"
            "**Project Geography**\n\n"
            "Northwest Liberia, with project sites in Lofa, Gbarpolu and Grand Cape Mount Counties."
        ),
        'status': 'ongoing',
        'county': 'national',
        'location_details': "Northwest Liberia: Lofa, Gbarpolu and Grand Cape Mount Counties",
        'donor': "GEF (Global Environmental Fund)",
        'implementing_agency': "Environmental Protection Agency (EPA)",
        'partners': "Society for the Conservation of Nature of Liberia (SCNL)",
        'start_date': date(2026, 5, 20),
        'completion_date': date(2030, 8, 31),
        'meta_description': (
            "PADEV delivers Component 2 of the Guinea Forest Integrated Programs (GFIP) across "
            "Lofa, Gbarpolu and Grand Cape Mount Counties in Northwest Liberia."
        ),
    },
    {
        'title': "Community-Based Forestry and Protected Area Management (CBFM)",
        'short_description': (
            "Three-phase programme promoting community-based conservation and sustainable use "
            "of natural resources across 20 community forests in Southeast Liberia."
        ),
        'description': (
            "**Project Summary**\n\n"
            "The project was implemented in three phases over three years and was designed:\n"
            "- To address policy, planning, livelihood and knowledge barriers by effectively "
            "promoting community-based conservation and sustainable use of natural resources, "
            "targeting 20 community forests through incentive-based conservation agreements.\n"
            "- To contribute to the conservation of biodiversity of global significance, "
            "including rare, endangered, threatened and endemic plant and animal species.\n\n"
            "**Project Outcome**\n\n"
            "- 6,720 direct and indirect beneficiaries reached with economically viable and "
            "sustainable livelihood programmes\n"
            "- 12 Village Saving and Loan Associations formed and strengthened\n"
            "- Institutional capacity of two community forest governance structures strengthened\n"
            "- Regulatory framework for community forest management improved\n\n"
            "**Project Geography**\n\n"
            "Southeast Liberia, with project sites in Grand Gedeh, River Gee, Sinoe and River "
            "Cess Counties."
        ),
        'status': 'ongoing',
        'county': 'national',
        'location_details': "Southeast Liberia: Grand Gedeh, River Gee, Sinoe and River Cess Counties",
        'donor': "Sweden Embassy in Liberia",
        'implementing_agency': "Forestry Development Authority (FDA)",
        'partners': "United Nations Development Programme (UNDP)",
        'start_date': date(2024, 1, 20),
        'completion_date': date(2026, 8, 20),
        'meta_description': (
            "Community-based forestry and protected area management programme reaching 6,720 "
            "beneficiaries across four counties in Southeast Liberia."
        ),
    },
    {
        'title': "National and Regional Consultations for the Proposed Liberia Forest Economy Project (LiFE-P)",
        'short_description': (
            "Stakeholder consultations across every stakeholder group to fulfil consultation "
            "requirements, raise awareness and build buy-in for the proposed Liberia Forest "
            "Economy Project."
        ),
        'description': (
            "Implemented on behalf of the Forestry Development Authority (FDA).\n\n"
            "**Objectives**\n\n"
            "- To fulfil stakeholder consultation requirements by facilitating stakeholder "
            "engagements across all stakeholder groups relevant to the effective implementation "
            "of the project.\n"
            "- To raise awareness about the project scope and content, inspire community trust "
            "and solicit stakeholder input, recognising their knowledge as integral to effective "
            "decision-making.\n"
            "- To refine project design choices, ensure safeguard measures for vulnerable groups, "
            "enhance grievance resolution, and secure the buy-in and partnerships needed to "
            "ensure the successful delivery of the project.\n\n"
            "**Project Outcome**\n\n"
            "- The national and regional stakeholder consultations were successfully held from "
            "19 to 30 June 2026.\n"
            "- One national and three regional consultations were held: the national event at "
            "Corina Hotel, Monrovia, and the regional consultations in Tubmanburg (Bomi County), "
            "Buchanan (Grand Bassa County) and Zwedru (Grand Gedeh County).\n"
            "- All events were coordinated with FDA.\n"
            "- The consultations engaged 158 stakeholders, comprising 18.9% female, 81.1% male "
            "and 17% youth.\n"
            "- Participants represented public sector institutions, forest governance structures, "
            "forest users, civil society organisations, not-for-profit organisations, private "
            "sector actors and local authorities.\n"
            "- Overall, stakeholders expressed strong support for the project, highlighting their "
            "gratitude for the opportunity to provide their insights, experiences and lessons to "
            "the development of the project.\n\n"
            "**Project Geography**\n\n"
            "Monrovia (national level), plus Northwest and Southeast priority landscapes covering "
            "six counties: Grand Cape Mount, Gbarpolu, Grand Bassa, River Cess, Sinoe and Grand "
            "Gedeh Counties."
        ),
        'status': 'ongoing',
        'county': 'national',
        'location_details': (
            "National: Monrovia plus Grand Cape Mount, Gbarpolu, Grand Bassa, River Cess, Sinoe "
            "and Grand Gedeh Counties"
        ),
        'donor': "The World Bank Group (WBG)",
        'implementing_agency': "Forestry Development Authority (FDA)",
        'partners': "United Nations Development Programme (UNDP)",
        'start_date': date(2026, 5, 18),
        'completion_date': date(2026, 12, 31),
        'meta_description': (
            "National and regional stakeholder consultations for the proposed Liberia Forest "
            "Economy Project, delivered on behalf of the Forestry Development Authority."
        ),
    },
    {
        'title': "USAID Conservation Works (CW)",
        'short_description': (
            "Biodiversity conservation and sustainable growth activity in five counties, where "
            "PADEV delivered livelihoods, enterprise and community conservation outputs."
        ),
        'description': (
            "**Project Summary**\n\n"
            "The Conservation Works (CW) activity aimed to conserve biodiversity while "
            "increasing sustainable economic growth in Liberia. Implementation centred on five "
            "strategic objectives:\n"
            "- SO 1: Area under improved conservation status increased\n"
            "- SO 2: Protection and management of target proposed and existing protected and "
            "conserved areas improved\n"
            "- SO 3: Prosperity and prospects for communities living around target proposed and "
            "existing protected and conserved areas increased\n"
            "- SO 4: Sustainable economic growth through conservation-compatible investment "
            "increased\n"
            "- SO 5: Integration of protected and conserved areas within One Health policy, "
            "planning and prioritisation in Liberia advanced\n\n"
            "**PADEV Role**\n\n"
            "PADEV was responsible for SO3: Prosperity and Prospects for Communities Living "
            "Around Target Proposed and Existing Protected and Conserved Areas Increased.\n\n"
            "**Project Outputs under PADEV**\n\n"
            "**IR 3.1 Productive capacity and market access strengthened**\n"
            "- Conducted a socioeconomic and livelihood assessment to understand community "
            "context and the socioeconomic status of individuals living in target landscapes.\n"
            "- Worked with farmers around proposed protected areas in the Southeast to create 8 "
            "seed gardens and build capacity in conservation-compatible agriculture. The seed "
            "gardens are multiplication sites that give farmers consistent access to planting "
            "materials.\n"
            "- Trained over 100 cassava growers on value addition to cassava products, covering "
            "food safety and handling, packaging, marketing and recordkeeping, including super "
            "gari, odorless fufu, high-quality cassava flour, cassava chips, cassava starch, "
            "attieke and fufu powder.\n"
            "- Distributed 3 sets of large cassava processing mills and accessories to the "
            "communities and facilitated the formation of cooperatives. Each group was provided "
            "with utensils, packaging materials, food safety items and maintenance tools for "
            "the mills.\n"
            "**IR 3.2 Access to capital and financial services for local communities improved**\n"
            "- 20 VSLAs established across target landscapes, with memberships ranging from "
            "25 to 30 individuals each.\n"
            "**IR 3.3 Conservation and green enterprises strengthened**\n"
            "- 391 individuals from 31 communities across southeast Liberia trained in "
            "sustainable beekeeping.\n"
            "- Start-up kits including beehives, smokers, harvesting knives, bee suits, "
            "containers, honey extractors, filters, spoons, wax and buckets distributed.\n"
            "- 16 entrepreneurs trained to produce environmentally friendly beehives to supply "
            "beekeepers and increase their stocks.\n"
            "**IR 2.3 Improved national, sub-national and community level appreciation of "
            "sustainable resource management and conservation**\n"
            "- Three matrix for change workshops to inform the development of the project "
            "communication strategy.\n"
            "- Three community-based theatre troupes trained to perform local dances, "
            "traditional folklore and live skits incorporating messages about conservation.\n"
            "- Awareness raised across project communities.\n"
            "- Peer-to-peer community outreaches conducted with consortium partners and the "
            "Federation of Liberian Youth (FLY).\n"
            "**Cross-cutting theme: gender**\n"
            "- Trained staff on the important role women play in sustainable forest management, "
            "covering social inclusion, the role of men and women in development programmes and "
            "gender mainstreaming.\n"
            "- A Gender and Social Inclusion officer was hired to promote inclusion and "
            "integrate gender in all project activities.\n\n"
            "**Project Geography**\n\n"
            "Five counties: Margibi (Marshall Wetlands), River Cess, Grand Kru, Sinoe and River "
            "Gee."
        ),
        'status': 'completed',
        'county': 'national',
        'location_details': "Margibi (Marshall Wetlands), River Cess, Grand Kru, Sinoe and River Gee",
        'donor': "USAID-Liberia",
        'implementing_agency': "Forestry Development Authority (FDA)",
        'partners': (
            "Consortium of five organisations:\n"
            "- Echo Health Alliance (EHA), prime\n"
            "- Fauna and Flora (F&F)\n"
            "- Partners in Development (PADEV)\n"
            "- Liberia Chimpanzee Rescue Program (LCRP)\n"
            "- Solimar International"
        ),
        'start_date': date(2021, 10, 26),
        'completion_date': date(2024, 8, 15),
        'meta_description': (
            "USAID Conservation Works: PADEV livelihoods, enterprise and community conservation "
            "outputs delivered across five counties in Liberia."
        ),
    },
    {
        'title': (
            "Strengthening Connectivity and Effective Management of the Sapo Forest Landscape "
            "and Conservation Corridors"
        ),
        'short_description': (
            "Reducing critical threats to biodiversity in the Sapo landscape through sustainable "
            "livelihoods, forest-friendly enterprises, market access and governance support."
        ),
        'description': (
            "**Project Summary**\n\n"
            "The overall goal of the grant was to reduce critical threats to biodiversity and "
            "contribute to the well-being of rural communities in the Sapo Landscape. PADEV's "
            "role was to:\n"
            "- Provide support to communities for the enhancement and diversification of "
            "sustainable livelihoods.\n"
            "- Facilitate the adoption of forest-friendly livelihood opportunities.\n"
            "- Improve access to markets and use of Participatory Market Systems Development "
            "(PMSD), providing the appropriate technical support on sustainable Non-Timber "
            "Forest Products (NTFP) harvest, e.g. beekeeping.\n\n"
            "**Project Outcome**\n\n"
            "- Improved the capacity of one community theatre troupe and equipped it with "
            "choreography materials to implement conservation outreach campaigns in the project "
            "sites.\n"
            "- Strengthened the institutional capacity of five governance structures and gave "
            "them basic skills in how to administer forest governance structures.\n"
            "- Gave small grants to five forest governance groups to increase their logistical "
            "capacity.\n"
            "- Established and supported 6 agricultural demonstration plots on the adoption of "
            "regenerative agriculture practices, trained and incentivised 60 farmers to manage "
            "the sites.\n"
            "- Strengthened the capacity of 100 local beekeepers, supplied them with 225 "
            "beehives and assorted beekeeping equipment, and linked them to a national "
            "association and market.\n"
            "- Established and supported 5 VSLAs in five communities closest to the Sapo "
            "National Park.\n\n"
            "**Project Geography**\n\n"
            "Southeastern Liberia: Sinoe and River Gee Counties."
        ),
        'status': 'completed',
        'county': 'national',
        'location_details': "Southeastern Liberia: Sinoe and River Gee Counties",
        'donor': "USAID West Africa",
        'implementing_agency': "Forestry Development Authority (FDA)",
        'partners': "Fauna & Flora as lead, with PADEV as a sub-grantee",
        'start_date': date(2023, 11, 1),
        'completion_date': date(2025, 2, 28),
        'meta_description': (
            "Sapo Forest Landscape connectivity grant: sustainable livelihoods, beekeeping, "
            "VSLAs and governance support in Sinoe and River Gee."
        ),
    },
]


class Command(BaseCommand):
    help = 'Load the five project factsheets (GFIP, CBFM, LiFE-P consultations, Conservation Works, Sapo) into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Overwrite every field of projects that already exist.',
        )

    def handle(self, *args, **options):
        force = options['force']
        created = updated = skipped = 0

        for data in PROJECTS:
            slug = slugify(data['title'])
            progress = progress_for(data['start_date'], data['completion_date'], data['status'])
            project = Project.objects.filter(slug=slug).first()

            if project is None:
                Project.objects.create(slug=slug, progress_percentage=progress, **data)
                created += 1
                self.stdout.write(self.style.SUCCESS('  created  %s' % data['title']))
                continue

            if force:
                for field, value in data.items():
                    setattr(project, field, value)
                project.slug = slug
                project.progress_percentage = progress
                project.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS('  updated  %s' % data['title']))
            else:
                skipped += 1
                self.stdout.write('  kept     %s (already in the database)' % data['title'])

        self.stdout.write(self.style.SUCCESS(
            'Projects ready: %d created, %d updated, %d left as-is.'
            % (created, updated, skipped)
        ))
