# -*- coding: utf-8 -*-

#  Copyright (c) 2019. Partners HealthCare and other members of
#  Forome Association
#
#  Developed by Sergey Trifonov based on contributions by Joel Krier,
#  Michael Bouzinier, Shamil Sunyaev and other members of Division of
#  Genetics, Brigham and Women's Hospital
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from app.view.attr import AttrH

#===============================================
def tuneAspects(dataset, aspects):
    view_gen = aspects["view_gen"]
    view_db = aspects["view_db"]

    _resetupAttr(view_gen, UCSC_AttrH(view_gen))
    _resetupAttr(view_db, GTEx_AttrH(view_gen))
    _resetupAttr(view_db, OMIM_AttrH(view_gen))
    _resetupAttr(view_db, GREV_AttrH(view_gen))
    _resetupAttr(view_db, MEDGEN_AttrH(view_gen))
    _resetupAttr(view_db, GeneCards_AttrH(view_gen))
    _resetupAttr(view_db, Beacons_AttrH(view_gen))
    _resetupAttr(view_db, PMID_AttrH(view_db))
    _resetupAttr(view_db, HGMD_PMID_AttrH(view_db))

    if "meta" not in dataset.getDataInfo():
        return
    case = dataset.getDataInfo()["meta"].get("case")
    samples = dataset.getDataInfo()["meta"].get("samples")
    _resetupAttr(view_gen,
        IGV_AttrH(dataset.getApp(), view_gen, case, samples))

#===============================================
def _resetupAttr(aspect_h, attr_h):
    idx1 = aspect_h.find(attr_h.getName().lower())
    idx2 = aspect_h.find(attr_h.getName())
    if idx1 >= 0:
        aspect_h.delAttr(aspect_h[idx1])
    if idx2 >= 0:
        aspect_h.delAttr(aspect_h[idx2])
    aspect_h.addAttr(attr_h, min(idx1, idx2)
        if min(idx1, idx2) >= 0 else max(idx1, idx2))

#===============================================
class UCSC_AttrH(AttrH):

    @staticmethod
    def makeLink(region_name, start, end, delta, assembly = "hg19"):
        return ("https://genome.ucsc.edu/cgi-bin/hgTracks?"
            + ("db=%s" % assembly)
            + ("&position=%s" % region_name)
            + "%3A" + str(max(0, start - delta))
            + "%2D" + str(end + delta))

    def __init__(self, view_gen):
        AttrH.__init__(self, "UCSC")
        self.setAspect(view_gen)

    def htmlRepr(self, obj, top_rec_obj):
        start = int(top_rec_obj["__data"]["start"])
        end = int(top_rec_obj["__data"]["end"])
        region_name = top_rec_obj["__data"]["seq_region_name"]
        link1 = self.makeLink(region_name, start, end, 10)
        link2 = self.makeLink(region_name, start, end, 250)
        return ('<table cellpadding="50"><tr><td>'
                + '<span title="Max Zoom In, 20bp range">'
                + ('<a href="%s" target="UCSC">Close Up</a>' % link1)
                + '</span> </td><td>'
                + '<span title="Zoom Out, 500bp range">'
                + ('<a href="%s" target="UCSC">Zoom Out</a>' % link2)
                + '</span> </td><td></table>', "norm")

#===============================================
class GTEx_AttrH(AttrH):

    @staticmethod
    def makeLink(gene):
        return "https://www.gtexportal.org/home/gene/" + gene

    def __init__(self, view):
        AttrH.__init__(self, "GTEx", title = "View on GTEx",
            tooltip = "View this gene on GTEx portal")
        self.setAspect(view)

    def htmlRepr(self, obj, top_rec_obj):
        genes = top_rec_obj["_view"]["general"]["genes"]
        if (not genes):
            return None
        links = []
        for gene in genes:
            url = self.makeLink(gene)
            links.append('<span title="GTEx">'
                + ('<a href="%s" target="GTEx">%s</a>' % (url, gene))
                + '</span>')
        return ('<br>'.join(links), "norm")

#===============================================
class OMIM_AttrH(AttrH):

    @staticmethod
    def makeLink(gene):
        return ("https://omim.org/search/?"
            + "index=geneMap&feild=approved_gene_symbol"
            + "&search=" + str(gene))

    def __init__(self, view):
        AttrH.__init__(self, "OMIM")
        self.setAspect(view)

    def htmlRepr(self, obj, top_rec_obj):
        genes = top_rec_obj["_view"]["general"]["genes"]
        if (not genes):
            return None
        links = []
        for gene in genes:
            url = self.makeLink(gene)
            links.append(
                ('<span title="Search OMIM Gene Map for %s">' % gene)
                + ('<a href="%s" target="OMIM">%s</a>' % (url, gene))
                + '</span>')
        return ('<br>'.join(links), "norm")

#===============================================
class GREV_AttrH(AttrH):

    @staticmethod
    def makeLink(gene):
        return "https://www.ncbi.nlm.nih.gov/books/NBK1116/?term=" + gene

    def __init__(self, view):
        AttrH.__init__(self, "GREV", title = "GeneReviews®",
            tooltip = "Search GeneReviews®")
        self.setAspect(view)

    def htmlRepr(self, obj, top_rec_obj):
        genes = top_rec_obj["_view"]["general"]["genes"]
        if (not genes):
            return None
        links = []
        for gene in genes:
            url = self.makeLink(gene)
            links.append(
                ('<span title="Search GeneReviews&reg; for %s">' % gene)
                + ('<a href="%s" target="GREV">%s</a>' % (url, gene))
                + '</span>')
        return ('<br>'.join(links), "norm")

#===============================================
class MEDGEN_AttrH(AttrH):

    @staticmethod
    def makeLink(gene):
        return ("https://www.ncbi.nlm.nih.gov/medgen/?term="
            + gene + "%5BGene%20Name%5D")

    def __init__(self, view):
        AttrH.__init__(self, "MEDGEN",
            title = "MedGen", tooltip = "Search MedGen")
        self.setAspect(view)

    def htmlRepr(self, obj, top_rec_obj):
        genes = top_rec_obj["_view"]["general"]["genes"]
        if (not genes):
            return None
        links = []
        for gene in genes:
            url = self.makeLink(gene)
            links.append(('<span title="Search MedGen for %s">' % gene)
                + ('<a href="%s" target="MEDGEN">%s</a>' % (url, gene))
                + '</span>')
        return ('<br>'.join(links), "norm")

class GeneCards_AttrH(AttrH):

    @staticmethod
    def makeLink(gene):
        return ("https://www.genecards.org/cgi-bin/carddisp.pl?gene=" + gene)

    def __init__(self, view):
        AttrH.__init__(self, "gene_cards",
            title = "GeneCards", tooltip = "Read GeneCards")
        self.setAspect(view)

    def htmlRepr(self, obj, top_rec_obj):
        genes = top_rec_obj["_view"]["general"]["genes"]
        if (not genes):
            return None
        links = []
        for gene in genes:
            url = self.makeLink(gene)
            links.append(('<span title="Read GeneCards for %s">' % gene)
                + ('<a href="%s" target="GeneCards">%s</a>' % (url, gene))
                + '</span>')
        return ('<br>'.join(links), "norm")

#===============================================
class Beacons_AttrH(AttrH):
    base = "https://beacon-network.org/#/search?"
    template = base + "pos={pos}&chrom={chrom}&allele={a}&ref={r}&rs=GRCh37"

    @staticmethod
    def makeLink(c, p, r, a):
        return (Beacons_AttrH.template.format(chrom=c,pos=p,r=r,a=a))

    def __init__(self, view):
        AttrH.__init__(self, "Beacons",
            title = "Beacons",
            tooltip = "Search what other organizations have "
                      "observed the same variant")
        self.setAspect(view)

    def htmlRepr(self, obj, top_rec_obj):
        c = top_rec_obj["__data"]["seq_region_name"]
        p = top_rec_obj["__data"]["start"]
        r = top_rec_obj["__data"]["ref"]
        a = top_rec_obj["__data"]["alt"]

        url = self.makeLink(c, p, r, a)
        link = (('<span title="Search Beacons">')
            + ('<a href="%s" target="Beacons">Search Beacons</a>' % (url))
            + '</span>')
        return (link, "norm")

#===============================================
class PMID_AttrH(AttrH):

    @staticmethod
    def makeLink(pmid):
        return ("https://www.ncbi.nlm.nih.gov/pubmed/{}".format(pmid))

    def __init__(self, view):
        AttrH.__init__(self, "references",
            title = "Found in PubMed", tooltip = "PubMed Abstracts")
        self.setAspect(view)

    def get_pmids(self, top_rec_obj):
        return top_rec_obj["_view"]["databases"]["references"]

    def htmlRepr(self, obj, top_rec_obj):
        pmids = self.get_pmids(top_rec_obj)
        if (not pmids):
            return None
        links = []
        for pmid in pmids:
            url = self.makeLink(pmid)
            links.append(('<span title="PubMed abstracts for %s">' % pmid)
                + ('<a href="%s" target="PubMed">%s</a>' % (url, pmid))
                + '</span>')
        return (', '.join(links), "norm")

#===============================================
class HGMD_PMID_AttrH(PMID_AttrH):

    def __init__(self, view):
        AttrH.__init__(self, "hgmd_pmids",
            title = "HGMD PMIDs", tooltip = "PubMed Abstracts (from HGMD)")
        self.setAspect(view)

    def get_pmids(self, top_rec_obj):
        return top_rec_obj["__data"]["hgmd_pmids"]

#===============================================
class IGV_AttrH(AttrH):
    def __init__(self, app, view_gen, case, samples):
        bam_base = app.getOption("http-bam-base")
        AttrH.__init__(self, "IGV",
            kind = "hidden" if bam_base is None else None)
        self.setAspect(view_gen)
        if bam_base is None:
            self.mPreUrl = None
            return

        # we are not sure what is the key to samples, so have to repackage
        samples = {info["id"]: info["name"] for info in samples.values()}
        samples_ids = sorted(samples)
        samples_names = [samples[id] for id in samples_ids]

        file_urls = ','.join([
            "%s/%s/%s.hg19.bam" % (bam_base, case, sample_id)
            for sample_id in samples_ids])
        self.mPreUrl = ("http://localhost:60151/load?file=%s"
            "&genome=hg19&merge=false&name=%s") % (
                file_urls, ",".join(samples_names))

    def htmlRepr(self, obj, top_rec_obj):
        if self.mPreUrl is None:
            return None
        start = int(top_rec_obj["__data"]["start"])
        end = int(top_rec_obj["__data"]["end"])
        link = self.mPreUrl + "&locus=%s:%d-%d" % (
            top_rec_obj["__data"]["seq_region_name"],
            max(0, start - 250), end + 250)
        return ('<table><tr><td><span title="For this link to work, '
            + 'make sure that IGV is running on your computer">'
            + ('<a href="%s">View Variant in IGV</a>' % link)
            + ' </span></td><td><a href='
            + '"https://software.broadinstitute.org/software/igv/download"'
            + ' target="_blank">'
            + 'Download IGV</a></td></tr></table>', "norm")
