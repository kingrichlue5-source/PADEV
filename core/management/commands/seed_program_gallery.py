"""
Seed the programme photo galleries from the files committed in seed_media/.

    python manage.py seed_program_gallery

The photos live in seed_media/program_gallery/<programme-slug>/ - committed
to git, because media/ itself is ignored. Every file is saved through Django's
storage, so on production it is uploaded to Cloudinary. The command is safe to
run on every deploy:

* a photo that is already in the database is never uploaded twice;
* a photo an editor deleted stays deleted (its file is still in storage);
* a cover image whose file has vanished is re-pointed at the first gallery
  photo, so programme cards keep showing a photograph.
"""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db.models import Max

from core.models import Program, ProgramImage

SEED_ROOT = Path(settings.BASE_DIR) / 'seed_media' / 'program_gallery'

# slug -> [(file name inside SEED_ROOT/<slug>/, caption verbatim from the client)]
GALLERIES = {
    'livelihood-enterprise-development': [
        (
            'livelihood-01-farm-inspection.jpg',
            'Johnny Socree, Leader of Smallholder Farmers in Sarbo District, '
            'Rivergee County Inspects His 1.5 ha farm of Intercropped with '
            'Plantain, Corn and Eddoes',
        ),
        (
            'livelihood-02-field-team-survey.jpg',
            'Laveto Akoi-Forkpa, Livelihood and Enterprise Development Lead '
            'and a Team of Enumerators and Field Extension Staff Out in the '
            'Field in Gbarpolu for a Gender Responsive Livelihood and '
            'Socioeconomic Survey',
        ),
        (
            'livelihood-03-field-work.jpg',
            '',
        ),
    ],
}


class Command(BaseCommand):
    help = 'Seed the programme photo galleries from seed_media/program_gallery/.'

    def handle(self, *args, **options):
        added = repaired = 0
        for slug, photos in GALLERIES.items():
            program = Program.objects.filter(slug=slug).first()
            if program is None:
                self.stdout.write(self.style.WARNING(
                    '  skipped  %s (programme not in the database)' % slug))
                continue
            next_order = (program.gallery_images.aggregate(m=Max('sort_order'))['m'] or 0) + 1
            for filename, caption in photos:
                if program.gallery_images.filter(image__endswith=filename).exists():
                    continue
                if self._file_stored('programs/gallery/%s' % filename):
                    continue  # uploaded before; an editor removed the row - keep it removed
                source = SEED_ROOT / slug / filename
                if not source.exists():
                    self.stdout.write(self.style.WARNING('  missing  %s' % source))
                    continue
                photo = ProgramImage(program=program, caption=caption, sort_order=next_order)
                with source.open('rb') as handle:
                    photo.image.save(filename, File(handle), save=True)
                next_order += 1
                added += 1
                self.stdout.write(self.style.SUCCESS(
                    '  added    %s -> %s' % (program.title, filename)))
            if self._repair_cover(program):
                repaired += 1
        summary = 'Gallery photos: %d added' % added
        if repaired:
            summary += ', %d cover image(s) repaired' % repaired
        self.stdout.write(self.style.SUCCESS(summary + '.'))

    def _file_stored(self, name):
        """True when the file is already in storage (or cannot be checked)."""
        try:
            return default_storage.exists(name)
        except Exception:
            # Can't reach storage: assume it is there rather than risk
            # uploading a duplicate copy of the photo.
            return True

    def _repair_cover(self, program):
        """Point a cover image whose file is gone at the first gallery photo."""
        cover_name = getattr(program.cover_image, 'name', None)
        if not cover_name:
            return False
        try:
            if default_storage.exists(cover_name):
                return False
        except Exception:
            return False
        first = program.gallery_images.first()
        if first is None:
            return False
        program.cover_image.name = first.image.name
        program.save(update_fields=['cover_image'])
        self.stdout.write(self.style.SUCCESS(
            '  repaired %s cover image -> %s' % (program.title, first.image.name)))
        return True
