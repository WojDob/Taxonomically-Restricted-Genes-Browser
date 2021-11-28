from browser.models import Genome, Taxon
from rest_framework import serializers


class GenomeSerializer(serializers.ModelSerializer):
    family = serializers.SerializerMethodField()
    genus = serializers.SerializerMethodField()

    class Meta:
        model = Genome
        fields = ["id", "accession", "name",
                  "family", "genus", "protein_count"]

    def get_family(self, object):
        return object.lineage.family.name

    def get_genus(self, object):
        return object.lineage.genus.name


class TaxonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxon
        fields = ["id", "name", "taxonomic_unit"]
