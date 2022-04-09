from browser.models import Genome, Taxon, TaxonomicallyRestrictedGene
from rest_framework import serializers


class TaxonomicallyRestrictedGeneListSerializer(serializers.ModelSerializer):
    specific_to = serializers.ReadOnlyField(source="specific_to.name")

    class Meta:
        model = TaxonomicallyRestrictedGene
        fields = ["id", "accession", "type", "specific_to"]


class TaxonomicallyRestrictedGeneDetailSerializer(serializers.ModelSerializer):
    specific_to = serializers.ReadOnlyField(source="specific_to.name")
    origin_genome = serializers.ReadOnlyField(source="origin_genome.name")

    class Meta:
        model = TaxonomicallyRestrictedGene
        fields = [
            "id",
            "accession",
            "origin_genome",
            "type",
            "specific_to",
            "length",
            "entropy",
            "disorder",
            "aggregation",
        ]


class GenomeListSerializer(serializers.ModelSerializer):
    family = serializers.SerializerMethodField()
    genus = serializers.SerializerMethodField()
    originating_trgs_count = serializers.SerializerMethodField()

    class Meta:
        model = Genome
        fields = [
            "id",
            "accession",
            "name",
            "family",
            "genus",
            "protein_count",
            "originating_trgs_count",
        ]

    def get_family(self, object):
        return object.lineage.family.name

    def get_genus(self, object):
        return object.lineage.genus.name

    def get_originating_trgs_count(self, object):
        return object.originating_trgs.count()


class GenomeDetailSerializer(serializers.ModelSerializer):
    family = serializers.SerializerMethodField()
    genus = serializers.SerializerMethodField()
    originating_trgs = TaxonomicallyRestrictedGeneListSerializer(
        read_only=True, many=True
    )

    class Meta:
        model = Genome
        fields = [
            "id",
            "accession",
            "name",
            "family",
            "genus",
            "protein_count",
            "originating_trgs",
        ]

    def get_family(self, object):
        return object.lineage.family.name

    def get_genus(self, object):
        return object.lineage.genus.name


class TaxonListSerializer(serializers.ModelSerializer):
    trgs_count = serializers.SerializerMethodField()

    class Meta:
        model = Taxon
        fields = ["id", "name", "taxonomic_unit", "trgs_count"]

    def get_trgs_count(self, object):
        return object.taxonomically_restricted_genes.count()


class TaxonDetailSerializer(serializers.ModelSerializer):
    taxonomically_restricted_genes = TaxonomicallyRestrictedGeneListSerializer(
        read_only=True, many=True
    )

    class Meta:
        model = Taxon
        fields = ["id", "name", "taxonomic_unit", "taxonomically_restricted_genes"]
