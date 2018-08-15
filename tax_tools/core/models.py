from django.db import models


# lets keep the core 990-centric models here
'''MANAGED METADATA MODELS'''
class Efile_Metadata(models.Model):
    # parent_sked = models.CharField(max_length=255, null=False)
    # parent_sked_part = models.CharField(max_length=255, null=False)
    ordering = models.FloatField(null=False)

    class Meta:
        abstract = True


class Schedule_Metadata(models.Model):
    name = models.CharField("parent schedule name", max_length=255, null=False)
    associated_forms = models.ManyToManyField('Schedule_Metadata', related_name='schedules')

    def __str__(self):
        return self.name


class Schedule_Part_Metadata(Efile_Metadata):
    part_name = models.CharField(
        "verbose schedule part name",
        max_length=255,
        null=False
    )
    part_key = models.CharField('schedule part key', max_length=255, null=False)
    parent_sked = models.ForeignKey(Schedule_Metadata, on_delete=models.CASCADE)
    xml_root = models.CharField(max_length=255, null=False)
    is_shell = models.BooleanField(null=False)

    def __str__(self):
        return self.part_name


class Field_Metadata(Efile_Metadata):
    in_a_group = models.BooleanField(null=False)
    db_table = models.CharField(max_length=255, null=False)
    db_name = models.CharField(max_length=255, null=False)
    attribute_name = models.CharField(max_length=255, null=False)
    xpath = models.CharField(max_length=510, null=False)
    irs_type = models.CharField(max_length=255, null=True)
    db_type = models.CharField(max_length=255, null=False)
    line_number = models.CharField(null=True, max_length=155)
    description = models.TextField(null=False)
    versions = models.CharField(max_length=255, null=False)
    parent_sked = models.ForeignKey(Schedule_Metadata, on_delete=models.CASCADE)
    parent_sked_part = models.ForeignKey(Schedule_Part_Metadata, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}: {1} ({2})".format(self.db_name, self.description, self.line_number)


class Organization(models.Model):
    '''This model represents a 1-1 org MySQL table generated from mgmt command scripts'''
    ein = models.CharField(db_index=True, max_length=31, null=False)
    taxpayer_name = models.CharField(db_index=True, max_length=255, blank=False, null=False)
    return_type = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return "{0} ({1})".format(self.taxpayer_name, self.ein)


class Fiscal_Year(models.Model):
    fiscal_year = models.IntegerField(db_index=True, null=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

'''
UNMANAGED 990 XML DATABASE MODELS
NOTE: THESE _NEED_ TO BE UPDATED CONCURRENTLY WITH ANY CHANGES TO THE MODELS IN THE DEPLOYED 990-XML-DATABASE AND DB NAMES IN 990-XML-METADATA
https://github.com/jsfenfen/990-xml-metadata
'''


class FilingFiling(models.Model):
    submission_year = models.IntegerField(blank=True, null=True)
    return_id = models.CharField(max_length=31, blank=True, null=True)
    filing_type = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=31)
    tax_period = models.IntegerField(blank=True, null=True)
    sub_date = models.CharField(max_length=31, blank=True, null=True)
    taxpayer_name = models.CharField(max_length=255, blank=True, null=True)
    return_type = models.CharField(max_length=7, blank=True, null=True)
    dln = models.CharField(max_length=31, blank=True, null=True)
    object_id = models.CharField(max_length=31, blank=True, null=True)
    schema_version = models.TextField(blank=True, null=True)
    tax_year = models.IntegerField(blank=True, null=True)
    parse_started = models.IntegerField(blank=True, null=True)
    parse_complete = models.IntegerField(blank=True, null=True)
    process_time = models.DateTimeField(blank=True, null=True)
    is_error = models.IntegerField(blank=True, null=True)
    key_error_count = models.IntegerField(blank=True, null=True)
    error_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.taxpayer_name

    class Meta:
        managed = False
        db_table = 'filing_filing'


class ReturnCntrctrcmpnstn(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    cntrctrcmpnstn_cntrctrnm = models.TextField(db_column='CntrctrCmpnstn_CntrctrNm', blank=True, null=True)  # Field name made lowercase.
    cntrctrnm_prsnnm = models.CharField(db_column='CntrctrNm_PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln1txt = models.CharField(db_column='BsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln2txt = models.CharField(db_column='BsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    cntrctrcmpnstn_cntrctraddrss = models.TextField(db_column='CntrctrCmpnstn_CntrctrAddrss', blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    cntrctrcmpnstn_srvcsdsc = models.CharField(db_column='CntrctrCmpnstn_SrvcsDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cntrctrcmpnstn_cmpnstnamt = models.BigIntegerField(db_column='CntrctrCmpnstn_CmpnstnAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_cntrctrcmpnstn'


class ReturnEzPart0(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    addrsschngind = models.CharField(db_column='AddrssChngInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    intlrtrnind = models.CharField(db_column='IntlRtrnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fnlrtrnind = models.CharField(db_column='FnlRtrnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    amnddrtrnind = models.CharField(db_column='AmnddRtrnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    grpexmptnnm = models.TextField(db_column='GrpExmptnNm', blank=True, null=True)  # Field name made lowercase.
    skdbntrqrdind = models.CharField(db_column='SkdBNtRqrdInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wbstaddrsstxt = models.CharField(db_column='WbstAddrssTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    oforgnztncrpind = models.CharField(db_column='OfOrgnztnCrpInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oforgnztntrstind = models.CharField(db_column='OfOrgnztnTrstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oforgnztnasscind = models.CharField(db_column='OfOrgnztnAsscInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oforgnztnothrind = models.CharField(db_column='OfOrgnztnOthrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oforgnztnothrdsc = models.CharField(db_column='OfOrgnztnOthrDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    grssrcptsamt = models.BigIntegerField(db_column='GrssRcptsAmt', blank=True, null=True)  # Field name made lowercase.
    mthdofaccntngcshind = models.CharField(db_column='MthdOfAccntngCshInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mthdofaccntngaccrlind = models.CharField(db_column='MthdOfAccntngAccrlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mthdofaccntngothrdsc = models.CharField(db_column='MthdOfAccntngOthrDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    orgnztn501c3ind = models.TextField(db_column='Orgnztn501c3Ind', blank=True, null=True)  # Field name made lowercase.
    orgnztn501cind = models.TextField(db_column='Orgnztn501cInd', blank=True, null=True)  # Field name made lowercase.
    orgnztn49471ntpfind = models.TextField(db_column='Orgnztn49471NtPFInd', blank=True, null=True)  # Field name made lowercase.
    orgnztn527ind = models.CharField(db_column='Orgnztn527Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ez_part_0'


class ReturnEzPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtiind = models.CharField(db_column='InfInSkdOPrtIInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cntrbtnsgftsgrntsetcamt = models.BigIntegerField(db_column='CntrbtnsGftsGrntsEtcAmt', blank=True, null=True)  # Field name made lowercase.
    prgrmsrvcrvnamt = models.BigIntegerField(db_column='PrgrmSrvcRvnAmt', blank=True, null=True)  # Field name made lowercase.
    mmbrshpdsamt = models.BigIntegerField(db_column='MmbrshpDsAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincmamt = models.BigIntegerField(db_column='InvstmntIncmAmt', blank=True, null=True)  # Field name made lowercase.
    slofasstsgrssamt = models.BigIntegerField(db_column='SlOfAsstsGrssAmt', blank=True, null=True)  # Field name made lowercase.
    cstorothrbssexpnsslamt = models.BigIntegerField(db_column='CstOrOthrBssExpnsSlAmt', blank=True, null=True)  # Field name made lowercase.
    gnorlssfrmslofasstsamt = models.BigIntegerField(db_column='GnOrLssFrmSlOfAsstsAmt', blank=True, null=True)  # Field name made lowercase.
    gmnggrssincmamt = models.TextField(db_column='GmngGrssIncmAmt', blank=True, null=True)  # Field name made lowercase.
    fndrsnggrssincmamt = models.TextField(db_column='FndrsngGrssIncmAmt', blank=True, null=True)  # Field name made lowercase.
    spclevntsdrctexpnssamt = models.BigIntegerField(db_column='SpclEvntsDrctExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    spclevntsntincmlssamt = models.BigIntegerField(db_column='SpclEvntsNtIncmLssAmt', blank=True, null=True)  # Field name made lowercase.
    grssslsofinvntryamt = models.BigIntegerField(db_column='GrssSlsOfInvntryAmt', blank=True, null=True)  # Field name made lowercase.
    cstofgdssldamt = models.BigIntegerField(db_column='CstOfGdsSldAmt', blank=True, null=True)  # Field name made lowercase.
    grssprftlssslsofinvntryamt = models.BigIntegerField(db_column='GrssPrftLssSlsOfInvntryAmt', blank=True, null=True)  # Field name made lowercase.
    othrrvnttlamt = models.BigIntegerField(db_column='OthrRvnTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlrvnamt = models.BigIntegerField(db_column='TtlRvnAmt', blank=True, null=True)  # Field name made lowercase.
    grntsandsmlramntspdamt = models.BigIntegerField(db_column='GrntsAndSmlrAmntsPdAmt', blank=True, null=True)  # Field name made lowercase.
    bnftspdtorfrmmbrsamt = models.BigIntegerField(db_column='BnftsPdTOrFrMmbrsAmt', blank=True, null=True)  # Field name made lowercase.
    slrsothrcmpemplbnftamt = models.BigIntegerField(db_column='SlrsOthrCmpEmplBnftAmt', blank=True, null=True)  # Field name made lowercase.
    fsandothrpymttindcntrctamt = models.BigIntegerField(db_column='FsAndOthrPymtTIndCntrctAmt', blank=True, null=True)  # Field name made lowercase.
    occpncyrntutltsandmntamt = models.BigIntegerField(db_column='OccpncyRntUtltsAndMntAmt', blank=True, null=True)  # Field name made lowercase.
    prntngpblctnspstgamt = models.BigIntegerField(db_column='PrntngPblctnsPstgAmt', blank=True, null=True)  # Field name made lowercase.
    othrexpnssttlamt = models.BigIntegerField(db_column='OthrExpnssTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlexpnssamt = models.BigIntegerField(db_column='TtlExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    excssordfctfryramt = models.BigIntegerField(db_column='ExcssOrDfctFrYrAmt', blank=True, null=True)  # Field name made lowercase.
    ntasstsorfndblncsboyamt = models.BigIntegerField(db_column='NtAsstsOrFndBlncsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrchngsinntasstsamt = models.BigIntegerField(db_column='OthrChngsInNtAsstsAmt', blank=True, null=True)  # Field name made lowercase.
    ntasstsorfndblncseoyamt = models.BigIntegerField(db_column='NtAsstsOrFndBlncsEOYAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ez_part_i'


class ReturnEzPartIi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    ez_infinskdoprtiiind = models.CharField(db_column='EZ_InfInSkdOPrtIIInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cshsvngsandinvstmnts_boyamt = models.BigIntegerField(db_column='CshSvngsAndInvstmnts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    cshsvngsandinvstmnts_eoyamt = models.BigIntegerField(db_column='CshSvngsAndInvstmnts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    lndandbldngs_boyamt = models.BigIntegerField(db_column='LndAndBldngs_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    lndandbldngs_eoyamt = models.BigIntegerField(db_column='LndAndBldngs_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrasststtldtl_boyamt = models.BigIntegerField(db_column='OthrAsstsTtlDtl_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrasststtldtl_eoyamt = models.BigIntegerField(db_column='OthrAsstsTtlDtl_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    frm990ttlassts_boyamt = models.BigIntegerField(db_column='Frm990TtlAssts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    frm990ttlassts_eoyamt = models.BigIntegerField(db_column='Frm990TtlAssts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    smofttllblts_boyamt = models.BigIntegerField(db_column='SmOfTtlLblts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    smofttllblts_eoyamt = models.BigIntegerField(db_column='SmOfTtlLblts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    ez_ntasstsorfndblncs = models.TextField(db_column='EZ_NtAsstsOrFndBlncs', blank=True, null=True)  # Field name made lowercase.
    ntasstsorfndblncs_boyamt = models.BigIntegerField(db_column='NtAsstsOrFndBlncs_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    ntasstsorfndblncs_eoyamt = models.BigIntegerField(db_column='NtAsstsOrFndBlncs_EOYAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ez_part_ii'


class ReturnEzPartIii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtiiiind = models.CharField(db_column='InfInSkdOPrtIIIInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prmryexmptprpstxt = models.TextField(db_column='PrmryExmptPrpsTxt', blank=True, null=True)  # Field name made lowercase.
    ttlprgrmsrvcexpnssamt = models.BigIntegerField(db_column='TtlPrgrmSrvcExpnssAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ez_part_iii'


class ReturnEzPartIv(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtivind = models.CharField(db_column='InfInSkdOPrtIVInd', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ez_part_iv'


class ReturnEzPartV(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    ez_infinskdoprtvind = models.CharField(db_column='EZ_InfInSkdOPrtVInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ez_actvtsntprvslyrptind = models.CharField(db_column='EZ_ActvtsNtPrvslyRptInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_chgmdtorgnzngdcntrptind = models.CharField(db_column='EZ_ChgMdTOrgnzngDcNtRptInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_orgnztnhdubiind = models.CharField(db_column='EZ_OrgnztnHdUBIInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_orgnztnfld990tind = models.CharField(db_column='EZ_OrgnztnFld990TInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_sbjcttprxytxind = models.TextField(db_column='EZ_SbjctTPrxyTxInd', blank=True, null=True)  # Field name made lowercase.
    ez_orgnztndsslvdetcind = models.TextField(db_column='EZ_OrgnztnDsslvdEtcInd', blank=True, null=True)  # Field name made lowercase.
    ez_drctindrctpltclexpndamt = models.BigIntegerField(db_column='EZ_DrctIndrctPltclExpndAmt', blank=True, null=True)  # Field name made lowercase.
    ez_frm1120plfldind = models.CharField(db_column='EZ_Frm1120PlFldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_mdlnstfrmoffcrsind = models.CharField(db_column='EZ_MdLnsTFrmOffcrsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_lnstfrmoffcrsamt = models.TextField(db_column='EZ_LnsTFrmOffcrsAmt', blank=True, null=True)  # Field name made lowercase.
    ez_inttnfsandcpcntramt = models.BigIntegerField(db_column='EZ_InttnFsAndCpCntrAmt', blank=True, null=True)  # Field name made lowercase.
    ez_grssrcptsfrpblcusamt = models.BigIntegerField(db_column='EZ_GrssRcptsFrPblcUsAmt', blank=True, null=True)  # Field name made lowercase.
    ez_tximpsdundrirc4911amt = models.BigIntegerField(db_column='EZ_TxImpsdUndrIRC4911Amt', blank=True, null=True)  # Field name made lowercase.
    ez_tximpsdundrirc4912amt = models.BigIntegerField(db_column='EZ_TxImpsdUndrIRC4912Amt', blank=True, null=True)  # Field name made lowercase.
    ez_tximpsdundrirc4955amt = models.BigIntegerField(db_column='EZ_TxImpsdUndrIRC4955Amt', blank=True, null=True)  # Field name made lowercase.
    ez_enggdinexcssbnfttrnsind = models.TextField(db_column='EZ_EnggdInExcssBnftTrnsInd', blank=True, null=True)  # Field name made lowercase.
    ez_tximpsdonorgnztnmgramt = models.BigIntegerField(db_column='EZ_TxImpsdOnOrgnztnMgrAmt', blank=True, null=True)  # Field name made lowercase.
    ez_txrmbrsdbyorgnztnamt = models.BigIntegerField(db_column='EZ_TxRmbrsdByOrgnztnAmt', blank=True, null=True)  # Field name made lowercase.
    ez_prhbtdtxshltrtrnsind = models.CharField(db_column='EZ_PrhbtdTxShltrTrnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_bksincrofdtl = models.TextField(db_column='EZ_BksInCrOfDtl', blank=True, null=True)  # Field name made lowercase.
    bksincrofdtl_prsnnm = models.CharField(db_column='BksInCrOfDtl_PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln1txt = models.CharField(db_column='BsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln2txt = models.CharField(db_column='BsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    bksincrofdtl_phnnm = models.CharField(db_column='BksInCrOfDtl_PhnNm', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ez_frgnfnnclaccntind = models.CharField(db_column='EZ_FrgnFnnclAccntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_frgnoffcind = models.CharField(db_column='EZ_FrgnOffcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_nectflngfrm990ind = models.TextField(db_column='EZ_NECTFlngFrm990Ind', blank=True, null=True)  # Field name made lowercase.
    ez_dnradvsdfndsind = models.CharField(db_column='EZ_DnrAdvsdFndsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_oprthsptlind = models.CharField(db_column='EZ_OprtHsptlInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_tnnngsrvcsprvddind = models.CharField(db_column='EZ_TnnngSrvcsPrvddInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_frm720fldind = models.CharField(db_column='EZ_Frm720FldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_rltdorgnztnctrlentind = models.CharField(db_column='EZ_RltdOrgnztnCtrlEntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_trnsctnwthcntrlentind = models.CharField(db_column='EZ_TrnsctnWthCntrlEntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ez_pltclcmpgnactyind = models.TextField(db_column='EZ_PltclCmpgnActyInd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ez_part_v'


class ReturnEzPartVi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtviind = models.CharField(db_column='InfInSkdOPrtVIInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lbbyngactvtsind = models.TextField(db_column='LbbyngActvtsInd', blank=True, null=True)  # Field name made lowercase.
    schloprtngind = models.TextField(db_column='SchlOprtngInd', blank=True, null=True)  # Field name made lowercase.
    trnsfrexmptnnchrtblrltdorgind = models.CharField(db_column='TrnsfrExmptNnChrtblRltdOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rltdorgsct527orgind = models.CharField(db_column='RltdOrgSct527OrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    othremplypdovr100kcnt = models.TextField(db_column='OthrEmplyPdOvr100kCnt', blank=True, null=True)  # Field name made lowercase.
    cntrctrcvdgrtrthn100kcnt = models.TextField(db_column='CntrctRcvdGrtrThn100KCnt', blank=True, null=True)  # Field name made lowercase.
    fldskdaind = models.CharField(db_column='FldSkdAInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prtviofcmpofhghstpdempltxt = models.TextField(db_column='PrtVIOfCmpOfHghstPdEmplTxt', blank=True, null=True)  # Field name made lowercase.
    prtvihghstpdcntrctprfsrvctxt = models.TextField(db_column='PrtVIHghstPdCntrctPrfSrvcTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ez_part_vi'


class ReturnEzcmpnstnhghstpdempl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    prsnnm = models.TextField(db_column='PrsnNm', blank=True, null=True)  # Field name made lowercase.
    ttltxt = models.CharField(db_column='TtlTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    avrghrsprwkrt = models.TextField(db_column='AvrgHrsPrWkRt', blank=True, null=True)  # Field name made lowercase.
    cmpnstnamt = models.BigIntegerField(db_column='CmpnstnAmt', blank=True, null=True)  # Field name made lowercase.
    emplybnftsamt = models.BigIntegerField(db_column='EmplyBnftsAmt', blank=True, null=True)  # Field name made lowercase.
    expnsaccntamt = models.BigIntegerField(db_column='ExpnsAccntAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ezcmpnstnhghstpdempl'


class ReturnEzcmpnstnofhghstpdcntrct(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    cmpnstnofhghstpdcntrct_bsnssnmln1 = models.TextField(db_column='CmpnstnOfHghstPdCntrct_BsnssNmLn1', blank=True, null=True)  # Field name made lowercase.
    cmpnstnofhghstpdcntrct_bsnssnmln2 = models.TextField(db_column='CmpnstnOfHghstPdCntrct_BsnssNmLn2', blank=True, null=True)  # Field name made lowercase.
    cmpnstnofhghstpdcntrct_prsnnm = models.TextField(db_column='CmpnstnOfHghstPdCntrct_PrsnNm', blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    cmpnstnofhghstpdcntrct_srvctxt = models.CharField(db_column='CmpnstnOfHghstPdCntrct_SrvcTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cmpnstnofhghstpdcntrct_cmpnstnamt = models.BigIntegerField(db_column='CmpnstnOfHghstPdCntrct_CmpnstnAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ezcmpnstnofhghstpdcntrct'


class ReturnEzfrgnfnnclaccntcntrycd(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    frgnfnnclaccntcntrycd = models.CharField(db_column='FrgnFnnclAccntCntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ezfrgnfnnclaccntcntrycd'


class ReturnEzfrgnoffccntrycd(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    frgnoffccntrycd = models.CharField(db_column='FrgnOffcCntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ezfrgnoffccntrycd'


class ReturnEzoffcrdrctrtrstempl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    prsnnm = models.TextField(db_column='PrsnNm', blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1 = models.TextField(db_column='BsnssNmLn1', blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2 = models.TextField(db_column='BsnssNmLn2', blank=True, null=True)  # Field name made lowercase.
    ttltxt = models.CharField(db_column='TtlTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    avrghrsprwkdvtdtpsrt = models.TextField(db_column='AvrgHrsPrWkDvtdTPsRt', blank=True, null=True)  # Field name made lowercase.
    cmpnstnamt = models.BigIntegerField(db_column='CmpnstnAmt', blank=True, null=True)  # Field name made lowercase.
    emplybnftprgrmamt = models.BigIntegerField(db_column='EmplyBnftPrgrmAmt', blank=True, null=True)  # Field name made lowercase.
    expnsaccntothrallwncamt = models.BigIntegerField(db_column='ExpnsAccntOthrAllwncAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ezoffcrdrctrtrstempl'


class ReturnEzprgrmsrvcaccmplshmnt(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dscrptnprgrmsrvcaccmtxt = models.TextField(db_column='DscrptnPrgrmSrvcAccmTxt', blank=True, null=True)  # Field name made lowercase.
    grntsandallctnsamt = models.BigIntegerField(db_column='GrntsAndAllctnsAmt', blank=True, null=True)  # Field name made lowercase.
    frgngrntsind = models.CharField(db_column='FrgnGrntsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prgrmsrvcexpnssamt = models.BigIntegerField(db_column='PrgrmSrvcExpnssAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ezprgrmsrvcaccmplshmnt'


class ReturnEzspclcndtndsc(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spclcndtndsc = models.TextField(db_column='SpclCndtnDsc', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ezspclcndtndsc'


class ReturnEzsttswhrcpyofrtrnisfldcd(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    sttswhrcpyofrtrnisfldcd = models.CharField(db_column='SttsWhrCpyOfRtrnIsFldCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_ezsttswhrcpyofrtrnisfldcd'


class ReturnFrgncntrycd(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    frgncntrycd = models.CharField(db_column='FrgnCntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_frgncntrycd'


class ReturnFrm990Prtviisctna(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    frm990prtviisctna = models.TextField(db_column='Frm990PrtVIISctnA', blank=True, null=True)  # Field name made lowercase.
    prsnnm = models.CharField(db_column='PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    ttltxt = models.CharField(db_column='TtlTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    avrghrsprwkrt = models.TextField(db_column='AvrgHrsPrWkRt', blank=True, null=True)  # Field name made lowercase.
    avrghrsprwkrltdorgrt = models.TextField(db_column='AvrgHrsPrWkRltdOrgRt', blank=True, null=True)  # Field name made lowercase.
    indvdltrstordrctrind = models.CharField(db_column='IndvdlTrstOrDrctrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    instttnltrstind = models.CharField(db_column='InstttnlTrstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    offcrind = models.CharField(db_column='OffcrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    kyemplyind = models.CharField(db_column='KyEmplyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hghstcmpnstdemplyind = models.CharField(db_column='HghstCmpnstdEmplyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    frmrofcrdrctrtrstind = models.CharField(db_column='FrmrOfcrDrctrTrstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rprtblcmpfrmorgamt = models.BigIntegerField(db_column='RprtblCmpFrmOrgAmt', blank=True, null=True)  # Field name made lowercase.
    rprtblcmpfrmrltdorgamt = models.BigIntegerField(db_column='RprtblCmpFrmRltdOrgAmt', blank=True, null=True)  # Field name made lowercase.
    othrcmpnstnamt = models.BigIntegerField(db_column='OthrCmpnstnAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_frm990prtviisctna'


class ReturnOthrexpnss(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dsc = models.CharField(db_column='Dsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ttlamt = models.BigIntegerField(db_column='TtlAmt', blank=True, null=True)  # Field name made lowercase.
    prgrmsrvcsamt = models.BigIntegerField(db_column='PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    mngmntandgnrlamt = models.BigIntegerField(db_column='MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    fndrsngamt = models.BigIntegerField(db_column='FndrsngAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_othrexpnss'


class ReturnOthrrvnmsc(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dsc = models.CharField(db_column='Dsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ttlrvnclmnamt = models.BigIntegerField(db_column='TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    rltdorexmptfncincmamt = models.BigIntegerField(db_column='RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    unrltdbsnssrvnamt = models.BigIntegerField(db_column='UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    exclsnamt = models.BigIntegerField(db_column='ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    bsnsscd = models.TextField(db_column='BsnssCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_othrrvnmsc'


class ReturnPart0(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    addrsschngind = models.CharField(db_column='AddrssChngInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    intlrtrnind = models.CharField(db_column='IntlRtrnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fnlrtrnind = models.CharField(db_column='FnlRtrnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    amnddrtrnind = models.CharField(db_column='AmnddRtrnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dngbsnssasnm_bsnssnmln1txt = models.CharField(db_column='DngBsnssAsNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    dngbsnssasnm_bsnssnmln2txt = models.CharField(db_column='DngBsnssAsNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    grssrcptsamt = models.BigIntegerField(db_column='GrssRcptsAmt', blank=True, null=True)  # Field name made lowercase.
    grprtrnfraffltsind = models.CharField(db_column='GrpRtrnFrAffltsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    allaffltsinclddind = models.TextField(db_column='AllAffltsInclddInd', blank=True, null=True)  # Field name made lowercase.
    grpexmptnnm = models.TextField(db_column='GrpExmptnNm', blank=True, null=True)  # Field name made lowercase.
    wbstaddrsstxt = models.CharField(db_column='WbstAddrssTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    oforgnztncrpind = models.CharField(db_column='OfOrgnztnCrpInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oforgnztntrstind = models.CharField(db_column='OfOrgnztnTrstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oforgnztnasscind = models.CharField(db_column='OfOrgnztnAsscInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oforgnztnothrind = models.CharField(db_column='OfOrgnztnOthrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othrorgnztndsc = models.CharField(db_column='OthrOrgnztnDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    frmtnyr = models.IntegerField(db_column='FrmtnYr', blank=True, null=True)  # Field name made lowercase.
    prncploffcrnm = models.CharField(db_column='PrncplOffcrNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    prncplofcrbsnssnm_bsnssnmln1txt = models.CharField(db_column='PrncplOfcrBsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    prncplofcrbsnssnm_bsnssnmln2txt = models.CharField(db_column='PrncplOfcrBsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    orgnztn501c3ind = models.CharField(db_column='Orgnztn501c3Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    orgnztn501cind = models.TextField(db_column='Orgnztn501cInd', blank=True, null=True)  # Field name made lowercase.
    orgnztn49471ntpfind = models.CharField(db_column='Orgnztn49471NtPFInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    orgnztn527ind = models.CharField(db_column='Orgnztn527Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lgldmclsttcd = models.CharField(db_column='LglDmclSttCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    lgldmclcntrycd = models.CharField(db_column='LglDmclCntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_0'


class ReturnPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    actvtyormssndsc = models.TextField(db_column='ActvtyOrMssnDsc', blank=True, null=True)  # Field name made lowercase.
    cntrcttrmntnind = models.CharField(db_column='CntrctTrmntnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vtngmmbrsgvrnngbdycnt = models.BigIntegerField(db_column='VtngMmbrsGvrnngBdyCnt', blank=True, null=True)  # Field name made lowercase.
    vtngmmbrsindpndntcnt = models.BigIntegerField(db_column='VtngMmbrsIndpndntCnt', blank=True, null=True)  # Field name made lowercase.
    ttlemplycnt = models.BigIntegerField(db_column='TtlEmplyCnt', blank=True, null=True)  # Field name made lowercase.
    ttlvlntrscnt = models.BigIntegerField(db_column='TtlVlntrsCnt', blank=True, null=True)  # Field name made lowercase.
    ttlgrssubiamt = models.BigIntegerField(db_column='TtlGrssUBIAmt', blank=True, null=True)  # Field name made lowercase.
    ntunrltdbstxblincmamt = models.BigIntegerField(db_column='NtUnrltdBsTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    pycntrbtnsgrntsamt = models.BigIntegerField(db_column='PYCntrbtnsGrntsAmt', blank=True, null=True)  # Field name made lowercase.
    cycntrbtnsgrntsamt = models.BigIntegerField(db_column='CYCntrbtnsGrntsAmt', blank=True, null=True)  # Field name made lowercase.
    pyprgrmsrvcrvnamt = models.BigIntegerField(db_column='PYPrgrmSrvcRvnAmt', blank=True, null=True)  # Field name made lowercase.
    cyprgrmsrvcrvnamt = models.BigIntegerField(db_column='CYPrgrmSrvcRvnAmt', blank=True, null=True)  # Field name made lowercase.
    pyinvstmntincmamt = models.BigIntegerField(db_column='PYInvstmntIncmAmt', blank=True, null=True)  # Field name made lowercase.
    cyinvstmntincmamt = models.BigIntegerField(db_column='CYInvstmntIncmAmt', blank=True, null=True)  # Field name made lowercase.
    pyothrrvnamt = models.BigIntegerField(db_column='PYOthrRvnAmt', blank=True, null=True)  # Field name made lowercase.
    cyothrrvnamt = models.BigIntegerField(db_column='CYOthrRvnAmt', blank=True, null=True)  # Field name made lowercase.
    pyttlrvnamt = models.BigIntegerField(db_column='PYTtlRvnAmt', blank=True, null=True)  # Field name made lowercase.
    cyttlrvnamt = models.BigIntegerField(db_column='CYTtlRvnAmt', blank=True, null=True)  # Field name made lowercase.
    pygrntsandsmlrpdamt = models.BigIntegerField(db_column='PYGrntsAndSmlrPdAmt', blank=True, null=True)  # Field name made lowercase.
    cygrntsandsmlrpdamt = models.BigIntegerField(db_column='CYGrntsAndSmlrPdAmt', blank=True, null=True)  # Field name made lowercase.
    pybnftspdtmmbrsamt = models.BigIntegerField(db_column='PYBnftsPdTMmbrsAmt', blank=True, null=True)  # Field name made lowercase.
    cybnftspdtmmbrsamt = models.BigIntegerField(db_column='CYBnftsPdTMmbrsAmt', blank=True, null=True)  # Field name made lowercase.
    pyslrscmpempbnftpdamt = models.BigIntegerField(db_column='PYSlrsCmpEmpBnftPdAmt', blank=True, null=True)  # Field name made lowercase.
    cyslrscmpempbnftpdamt = models.BigIntegerField(db_column='CYSlrsCmpEmpBnftPdAmt', blank=True, null=True)  # Field name made lowercase.
    pyttlprffndrsngexpnsamt = models.BigIntegerField(db_column='PYTtlPrfFndrsngExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    cyttlprffndrsngexpnsamt = models.BigIntegerField(db_column='CYTtlPrfFndrsngExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    cyttlfndrsngexpnsamt = models.BigIntegerField(db_column='CYTtlFndrsngExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    pyothrexpnssamt = models.BigIntegerField(db_column='PYOthrExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    cyothrexpnssamt = models.BigIntegerField(db_column='CYOthrExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    pyttlexpnssamt = models.BigIntegerField(db_column='PYTtlExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    cyttlexpnssamt = models.BigIntegerField(db_column='CYTtlExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    pyrvnslssexpnssamt = models.BigIntegerField(db_column='PYRvnsLssExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    cyrvnslssexpnssamt = models.BigIntegerField(db_column='CYRvnsLssExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    ttlasstsboyamt = models.BigIntegerField(db_column='TtlAsstsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttlasstseoyamt = models.BigIntegerField(db_column='TtlAsstsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttllbltsboyamt = models.BigIntegerField(db_column='TtlLbltsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttllbltseoyamt = models.BigIntegerField(db_column='TtlLbltsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    ntasstsorfndblncsboyamt = models.BigIntegerField(db_column='NtAsstsOrFndBlncsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    ntasstsorfndblncseoyamt = models.BigIntegerField(db_column='NtAsstsOrFndBlncsEOYAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_i'


class ReturnPartIii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtiiiind = models.CharField(db_column='InfInSkdOPrtIIIInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mssndsc = models.TextField(db_column='MssnDsc', blank=True, null=True)  # Field name made lowercase.
    sgnfcntnwprgrmsrvcind = models.CharField(db_column='SgnfcntNwPrgrmSrvcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sgnfcntchngind = models.CharField(db_column='SgnfcntChngInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    actvtycd = models.BigIntegerField(db_column='ActvtyCd', blank=True, null=True)  # Field name made lowercase.
    expnsamt = models.BigIntegerField(db_column='ExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    grntamt = models.BigIntegerField(db_column='GrntAmt', blank=True, null=True)  # Field name made lowercase.
    rvnamt = models.BigIntegerField(db_column='RvnAmt', blank=True, null=True)  # Field name made lowercase.
    dsc = models.TextField(db_column='Dsc', blank=True, null=True)  # Field name made lowercase.
    prgsrvcaccmacty2_actvtycd = models.BigIntegerField(db_column='PrgSrvcAccmActy2_ActvtyCd', blank=True, null=True)  # Field name made lowercase.
    prgsrvcaccmacty2_expnsamt = models.BigIntegerField(db_column='PrgSrvcAccmActy2_ExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    prgsrvcaccmacty2_grntamt = models.BigIntegerField(db_column='PrgSrvcAccmActy2_GrntAmt', blank=True, null=True)  # Field name made lowercase.
    prgsrvcaccmacty2_rvnamt = models.BigIntegerField(db_column='PrgSrvcAccmActy2_RvnAmt', blank=True, null=True)  # Field name made lowercase.
    prgsrvcaccmacty2_dsc = models.TextField(db_column='PrgSrvcAccmActy2_Dsc', blank=True, null=True)  # Field name made lowercase.
    prgsrvcaccmacty3_actvtycd = models.BigIntegerField(db_column='PrgSrvcAccmActy3_ActvtyCd', blank=True, null=True)  # Field name made lowercase.
    prgsrvcaccmacty3_expnsamt = models.BigIntegerField(db_column='PrgSrvcAccmActy3_ExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    prgsrvcaccmacty3_grntamt = models.BigIntegerField(db_column='PrgSrvcAccmActy3_GrntAmt', blank=True, null=True)  # Field name made lowercase.
    prgsrvcaccmacty3_rvnamt = models.BigIntegerField(db_column='PrgSrvcAccmActy3_RvnAmt', blank=True, null=True)  # Field name made lowercase.
    prgsrvcaccmacty3_dsc = models.TextField(db_column='PrgSrvcAccmActy3_Dsc', blank=True, null=True)  # Field name made lowercase.
    ttlothrprgsrvcexpnsamt = models.BigIntegerField(db_column='TtlOthrPrgSrvcExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlothrprgsrvcgrntamt = models.BigIntegerField(db_column='TtlOthrPrgSrvcGrntAmt', blank=True, null=True)  # Field name made lowercase.
    ttlothrprgsrvcrvnamt = models.BigIntegerField(db_column='TtlOthrPrgSrvcRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ttlprgrmsrvcexpnssamt = models.BigIntegerField(db_column='TtlPrgrmSrvcExpnssAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_iii'


class ReturnPartIv(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dscrbdinsctn501c3ind = models.TextField(db_column='DscrbdInSctn501c3Ind', blank=True, null=True)  # Field name made lowercase.
    skdbrqrdind = models.TextField(db_column='SkdBRqrdInd', blank=True, null=True)  # Field name made lowercase.
    pltclcmpgnactyind = models.TextField(db_column='PltclCmpgnActyInd', blank=True, null=True)  # Field name made lowercase.
    lbbyngactvtsind = models.TextField(db_column='LbbyngActvtsInd', blank=True, null=True)  # Field name made lowercase.
    sbjcttprxytxind = models.TextField(db_column='SbjctTPrxyTxInd', blank=True, null=True)  # Field name made lowercase.
    dnradvsdfndind = models.TextField(db_column='DnrAdvsdFndInd', blank=True, null=True)  # Field name made lowercase.
    cnsrvtnesmntsind = models.TextField(db_column='CnsrvtnEsmntsInd', blank=True, null=True)  # Field name made lowercase.
    cllctnsofartind = models.TextField(db_column='CllctnsOfArtInd', blank=True, null=True)  # Field name made lowercase.
    crdtcnslngind = models.TextField(db_column='CrdtCnslngInd', blank=True, null=True)  # Field name made lowercase.
    tmporprmnntendwmntsind = models.TextField(db_column='TmpOrPrmnntEndwmntsInd', blank=True, null=True)  # Field name made lowercase.
    rprtlndbldngeqpmntind = models.TextField(db_column='RprtLndBldngEqpmntInd', blank=True, null=True)  # Field name made lowercase.
    rprtinvstmntsothrscind = models.TextField(db_column='RprtInvstmntsOthrScInd', blank=True, null=True)  # Field name made lowercase.
    rprtprgrmrltdinvstind = models.TextField(db_column='RprtPrgrmRltdInvstInd', blank=True, null=True)  # Field name made lowercase.
    rprtothrasstsind = models.TextField(db_column='RprtOthrAsstsInd', blank=True, null=True)  # Field name made lowercase.
    rprtothrlbltsind = models.TextField(db_column='RprtOthrLbltsInd', blank=True, null=True)  # Field name made lowercase.
    incldfin48ftntind = models.TextField(db_column='IncldFIN48FtntInd', blank=True, null=True)  # Field name made lowercase.
    indpndntadtfnclstmtind = models.TextField(db_column='IndpndntAdtFnclStmtInd', blank=True, null=True)  # Field name made lowercase.
    cnsldtdadtfnclstmtind = models.TextField(db_column='CnsldtdAdtFnclStmtInd', blank=True, null=True)  # Field name made lowercase.
    schloprtngind = models.TextField(db_column='SchlOprtngInd', blank=True, null=True)  # Field name made lowercase.
    frgnoffcind = models.CharField(db_column='FrgnOffcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frgnactvtsind = models.TextField(db_column='FrgnActvtsInd', blank=True, null=True)  # Field name made lowercase.
    mrthn5000ktorgind = models.TextField(db_column='MrThn5000KTOrgInd', blank=True, null=True)  # Field name made lowercase.
    mrthn5000ktindvdlsind = models.TextField(db_column='MrThn5000KTIndvdlsInd', blank=True, null=True)  # Field name made lowercase.
    prfssnlfndrsngind = models.TextField(db_column='PrfssnlFndrsngInd', blank=True, null=True)  # Field name made lowercase.
    fndrsngactvtsind = models.TextField(db_column='FndrsngActvtsInd', blank=True, null=True)  # Field name made lowercase.
    gmngactvtsind = models.TextField(db_column='GmngActvtsInd', blank=True, null=True)  # Field name made lowercase.
    oprthsptlind = models.TextField(db_column='OprtHsptlInd', blank=True, null=True)  # Field name made lowercase.
    adtdfnnclstmtattind = models.TextField(db_column='AdtdFnnclStmtAttInd', blank=True, null=True)  # Field name made lowercase.
    grntstorgnztnsind = models.TextField(db_column='GrntsTOrgnztnsInd', blank=True, null=True)  # Field name made lowercase.
    grntstindvdlsind = models.TextField(db_column='GrntsTIndvdlsInd', blank=True, null=True)  # Field name made lowercase.
    skdjrqrdind = models.TextField(db_column='SkdJRqrdInd', blank=True, null=True)  # Field name made lowercase.
    txexmptbndsind = models.TextField(db_column='TxExmptBndsInd', blank=True, null=True)  # Field name made lowercase.
    invsttxexmptbndsind = models.CharField(db_column='InvstTxExmptBndsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    escrwaccntind = models.CharField(db_column='EscrwAccntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    onbhlfofissrind = models.CharField(db_column='OnBhlfOfIssrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    enggdinexcssbnfttrnsind = models.TextField(db_column='EnggdInExcssBnftTrnsInd', blank=True, null=True)  # Field name made lowercase.
    pyexcssbnfttrnsind = models.TextField(db_column='PYExcssBnftTrnsInd', blank=True, null=True)  # Field name made lowercase.
    lnotstndngind = models.TextField(db_column='LnOtstndngInd', blank=True, null=True)  # Field name made lowercase.
    grnttrltdprsnind = models.TextField(db_column='GrntTRltdPrsnInd', blank=True, null=True)  # Field name made lowercase.
    bsnssrlnwthorgmmind = models.TextField(db_column='BsnssRlnWthOrgMmInd', blank=True, null=True)  # Field name made lowercase.
    bsnssrlnwthfmmmind = models.TextField(db_column='BsnssRlnWthFmMmInd', blank=True, null=True)  # Field name made lowercase.
    bsnssrlnwthoffcrentind = models.TextField(db_column='BsnssRlnWthOffcrEntInd', blank=True, null=True)  # Field name made lowercase.
    ddctblnncshcntrind = models.TextField(db_column='DdctblNnCshCntrInd', blank=True, null=True)  # Field name made lowercase.
    ddctblartcntrbtnind = models.TextField(db_column='DdctblArtCntrbtnInd', blank=True, null=True)  # Field name made lowercase.
    trmntoprtnsind = models.TextField(db_column='TrmntOprtnsInd', blank=True, null=True)  # Field name made lowercase.
    prtllqdtnind = models.TextField(db_column='PrtlLqdtnInd', blank=True, null=True)  # Field name made lowercase.
    dsrgrddenttyind = models.TextField(db_column='DsrgrddEnttyInd', blank=True, null=True)  # Field name made lowercase.
    rltdenttyind = models.TextField(db_column='RltdEnttyInd', blank=True, null=True)  # Field name made lowercase.
    rltdorgnztnctrlentind = models.CharField(db_column='RltdOrgnztnCtrlEntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    trnsctnwthcntrlentind = models.TextField(db_column='TrnsctnWthCntrlEntInd', blank=True, null=True)  # Field name made lowercase.
    trnsfrexmptnnchrtblrltdorgind = models.TextField(db_column='TrnsfrExmptNnChrtblRltdOrgInd', blank=True, null=True)  # Field name made lowercase.
    actvtscndctdprtshpind = models.TextField(db_column='ActvtsCndctdPrtshpInd', blank=True, null=True)  # Field name made lowercase.
    skdorqrdind = models.CharField(db_column='SkdORqrdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_iv'


class ReturnPartIx(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtixind = models.CharField(db_column='InfInSkdOPrtIXInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsprffndrsng = models.TextField(db_column='FsFrSrvcsPrfFndrsng', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsprffndrsng_ttlamt = models.BigIntegerField(db_column='FsFrSrvcsPrfFndrsng_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsprffndrsng_fndrsngamt = models.BigIntegerField(db_column='FsFrSrvcsPrfFndrsng_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    jntcstsind = models.CharField(db_column='JntCstsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    advrtsng_ttlamt = models.BigIntegerField(db_column='Advrtsng_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    allothrexpnss_ttlamt = models.BigIntegerField(db_column='AllOthrExpnss_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    bnftstmmbrs_ttlamt = models.BigIntegerField(db_column='BnftsTMmbrs_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    cmpcrrntofcrdrctrs_ttlamt = models.BigIntegerField(db_column='CmpCrrntOfcrDrctrs_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    cmpdsqlprsns_ttlamt = models.BigIntegerField(db_column='CmpDsqlPrsns_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    cnfrncsmtngs_ttlamt = models.BigIntegerField(db_column='CnfrncsMtngs_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    dprctndpltn_ttlamt = models.BigIntegerField(db_column='DprctnDpltn_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsaccntng_ttlamt = models.BigIntegerField(db_column='FsFrSrvcsAccntng_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcslgl_ttlamt = models.BigIntegerField(db_column='FsFrSrvcsLgl_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcslbbyng_ttlamt = models.BigIntegerField(db_column='FsFrSrvcsLbbyng_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsmngmnt_ttlamt = models.BigIntegerField(db_column='FsFrSrvcsMngmnt_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsothr_ttlamt = models.BigIntegerField(db_column='FsFrSrvcsOthr_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcinvstmgmntfs_ttlamt = models.BigIntegerField(db_column='FsFrSrvcInvstMgmntFs_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    frgngrnts_ttlamt = models.BigIntegerField(db_column='FrgnGrnts_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    grntstdmstcindvdls_ttlamt = models.BigIntegerField(db_column='GrntsTDmstcIndvdls_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    grntstdmstcorgs_ttlamt = models.BigIntegerField(db_column='GrntsTDmstcOrgs_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    infrmtntchnlgy_ttlamt = models.BigIntegerField(db_column='InfrmtnTchnlgy_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    insrnc_ttlamt = models.BigIntegerField(db_column='Insrnc_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    intrst_ttlamt = models.BigIntegerField(db_column='Intrst_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    occpncy_ttlamt = models.BigIntegerField(db_column='Occpncy_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    offcexpnss_ttlamt = models.BigIntegerField(db_column='OffcExpnss_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    othremplybnfts_ttlamt = models.BigIntegerField(db_column='OthrEmplyBnfts_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    othrslrsandwgs_ttlamt = models.BigIntegerField(db_column='OthrSlrsAndWgs_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    pymntstafflts_ttlamt = models.BigIntegerField(db_column='PymntsTAfflts_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    pyrlltxs_ttlamt = models.BigIntegerField(db_column='PyrllTxs_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    pnsnplncntrbtns_ttlamt = models.BigIntegerField(db_column='PnsnPlnCntrbtns_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    pymttrvlentrtnmntpbofcl_ttlamt = models.BigIntegerField(db_column='PymtTrvlEntrtnmntPbOfcl_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    rylts_ttlamt = models.BigIntegerField(db_column='Rylts_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlfnctnlexpnss_ttlamt = models.BigIntegerField(db_column='TtlFnctnlExpnss_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttljntcsts_ttlamt = models.BigIntegerField(db_column='TtlJntCsts_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    trvl_ttlamt = models.BigIntegerField(db_column='Trvl_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    advrtsng_prgrmsrvcsamt = models.BigIntegerField(db_column='Advrtsng_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    allothrexpnss_prgrmsrvcsamt = models.BigIntegerField(db_column='AllOthrExpnss_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    bnftstmmbrs_prgrmsrvcsamt = models.BigIntegerField(db_column='BnftsTMmbrs_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    cmpcrrntofcrdrctrs_prgrmsrvcsamt = models.BigIntegerField(db_column='CmpCrrntOfcrDrctrs_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    cmpdsqlprsns_prgrmsrvcsamt = models.BigIntegerField(db_column='CmpDsqlPrsns_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    cnfrncsmtngs_prgrmsrvcsamt = models.BigIntegerField(db_column='CnfrncsMtngs_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    dprctndpltn_prgrmsrvcsamt = models.BigIntegerField(db_column='DprctnDpltn_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsaccntng_prgrmsrvcsamt = models.BigIntegerField(db_column='FsFrSrvcsAccntng_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcslgl_prgrmsrvcsamt = models.BigIntegerField(db_column='FsFrSrvcsLgl_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcslbbyng_prgrmsrvcsamt = models.BigIntegerField(db_column='FsFrSrvcsLbbyng_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsmngmnt_prgrmsrvcsamt = models.BigIntegerField(db_column='FsFrSrvcsMngmnt_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsothr_prgrmsrvcsamt = models.BigIntegerField(db_column='FsFrSrvcsOthr_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcinvstmgmntfs_prgrmsrvcsamt = models.BigIntegerField(db_column='FsFrSrvcInvstMgmntFs_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    frgngrnts_prgrmsrvcsamt = models.BigIntegerField(db_column='FrgnGrnts_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    grntstdmstcindvdls_prgrmsrvcsamt = models.BigIntegerField(db_column='GrntsTDmstcIndvdls_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    grntstdmstcorgs_prgrmsrvcsamt = models.BigIntegerField(db_column='GrntsTDmstcOrgs_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    infrmtntchnlgy_prgrmsrvcsamt = models.BigIntegerField(db_column='InfrmtnTchnlgy_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    insrnc_prgrmsrvcsamt = models.BigIntegerField(db_column='Insrnc_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    intrst_prgrmsrvcsamt = models.BigIntegerField(db_column='Intrst_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    occpncy_prgrmsrvcsamt = models.BigIntegerField(db_column='Occpncy_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    offcexpnss_prgrmsrvcsamt = models.BigIntegerField(db_column='OffcExpnss_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    othremplybnfts_prgrmsrvcsamt = models.BigIntegerField(db_column='OthrEmplyBnfts_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    othrslrsandwgs_prgrmsrvcsamt = models.BigIntegerField(db_column='OthrSlrsAndWgs_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    pymntstafflts_prgrmsrvcsamt = models.BigIntegerField(db_column='PymntsTAfflts_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    pyrlltxs_prgrmsrvcsamt = models.BigIntegerField(db_column='PyrllTxs_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    pnsnplncntrbtns_prgrmsrvcsamt = models.BigIntegerField(db_column='PnsnPlnCntrbtns_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    pymttrvlentrtnmntpbofcl_prgrmsrvcsamt = models.BigIntegerField(db_column='PymtTrvlEntrtnmntPbOfcl_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    rylts_prgrmsrvcsamt = models.BigIntegerField(db_column='Rylts_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlfnctnlexpnss_prgrmsrvcsamt = models.BigIntegerField(db_column='TtlFnctnlExpnss_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    ttljntcsts_prgrmsrvcsamt = models.BigIntegerField(db_column='TtlJntCsts_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    trvl_prgrmsrvcsamt = models.BigIntegerField(db_column='Trvl_PrgrmSrvcsAmt', blank=True, null=True)  # Field name made lowercase.
    advrtsng_mngmntandgnrlamt = models.BigIntegerField(db_column='Advrtsng_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    allothrexpnss_mngmntandgnrlamt = models.BigIntegerField(db_column='AllOthrExpnss_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    cmpcrrntofcrdrctrs_mngmntandgnrlamt = models.BigIntegerField(db_column='CmpCrrntOfcrDrctrs_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    cmpdsqlprsns_mngmntandgnrlamt = models.BigIntegerField(db_column='CmpDsqlPrsns_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    cnfrncsmtngs_mngmntandgnrlamt = models.BigIntegerField(db_column='CnfrncsMtngs_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    dprctndpltn_mngmntandgnrlamt = models.BigIntegerField(db_column='DprctnDpltn_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsaccntng_mngmntandgnrlamt = models.BigIntegerField(db_column='FsFrSrvcsAccntng_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcslgl_mngmntandgnrlamt = models.BigIntegerField(db_column='FsFrSrvcsLgl_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcslbbyng_mngmntandgnrlamt = models.BigIntegerField(db_column='FsFrSrvcsLbbyng_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsmngmnt_mngmntandgnrlamt = models.BigIntegerField(db_column='FsFrSrvcsMngmnt_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsothr_mngmntandgnrlamt = models.BigIntegerField(db_column='FsFrSrvcsOthr_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcinvstmgmntfs_mngmntandgnrlamt = models.BigIntegerField(db_column='FsFrSrvcInvstMgmntFs_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    infrmtntchnlgy_mngmntandgnrlamt = models.BigIntegerField(db_column='InfrmtnTchnlgy_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    insrnc_mngmntandgnrlamt = models.BigIntegerField(db_column='Insrnc_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    intrst_mngmntandgnrlamt = models.BigIntegerField(db_column='Intrst_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    occpncy_mngmntandgnrlamt = models.BigIntegerField(db_column='Occpncy_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    offcexpnss_mngmntandgnrlamt = models.BigIntegerField(db_column='OffcExpnss_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    othremplybnfts_mngmntandgnrlamt = models.BigIntegerField(db_column='OthrEmplyBnfts_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    othrslrsandwgs_mngmntandgnrlamt = models.BigIntegerField(db_column='OthrSlrsAndWgs_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    pymntstafflts_mngmntandgnrlamt = models.BigIntegerField(db_column='PymntsTAfflts_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    pyrlltxs_mngmntandgnrlamt = models.BigIntegerField(db_column='PyrllTxs_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    pnsnplncntrbtns_mngmntandgnrlamt = models.BigIntegerField(db_column='PnsnPlnCntrbtns_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    pymttrvlentrtnmntpbofcl_mngmntandgnrlamt = models.BigIntegerField(db_column='PymtTrvlEntrtnmntPbOfcl_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    rylts_mngmntandgnrlamt = models.BigIntegerField(db_column='Rylts_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlfnctnlexpnss_mngmntandgnrlamt = models.BigIntegerField(db_column='TtlFnctnlExpnss_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    ttljntcsts_mngmntandgnrlamt = models.BigIntegerField(db_column='TtlJntCsts_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    trvl_mngmntandgnrlamt = models.BigIntegerField(db_column='Trvl_MngmntAndGnrlAmt', blank=True, null=True)  # Field name made lowercase.
    advrtsng_fndrsngamt = models.BigIntegerField(db_column='Advrtsng_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    allothrexpnss_fndrsngamt = models.BigIntegerField(db_column='AllOthrExpnss_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    cmpcrrntofcrdrctrs_fndrsngamt = models.BigIntegerField(db_column='CmpCrrntOfcrDrctrs_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    cmpdsqlprsns_fndrsngamt = models.BigIntegerField(db_column='CmpDsqlPrsns_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    cnfrncsmtngs_fndrsngamt = models.BigIntegerField(db_column='CnfrncsMtngs_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    dprctndpltn_fndrsngamt = models.BigIntegerField(db_column='DprctnDpltn_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsaccntng_fndrsngamt = models.BigIntegerField(db_column='FsFrSrvcsAccntng_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcslgl_fndrsngamt = models.BigIntegerField(db_column='FsFrSrvcsLgl_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcslbbyng_fndrsngamt = models.BigIntegerField(db_column='FsFrSrvcsLbbyng_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsmngmnt_fndrsngamt = models.BigIntegerField(db_column='FsFrSrvcsMngmnt_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcsothr_fndrsngamt = models.BigIntegerField(db_column='FsFrSrvcsOthr_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    fsfrsrvcinvstmgmntfs_fndrsngamt = models.BigIntegerField(db_column='FsFrSrvcInvstMgmntFs_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    infrmtntchnlgy_fndrsngamt = models.BigIntegerField(db_column='InfrmtnTchnlgy_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    insrnc_fndrsngamt = models.BigIntegerField(db_column='Insrnc_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    intrst_fndrsngamt = models.BigIntegerField(db_column='Intrst_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    occpncy_fndrsngamt = models.BigIntegerField(db_column='Occpncy_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    offcexpnss_fndrsngamt = models.BigIntegerField(db_column='OffcExpnss_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    othremplybnfts_fndrsngamt = models.BigIntegerField(db_column='OthrEmplyBnfts_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    othrslrsandwgs_fndrsngamt = models.BigIntegerField(db_column='OthrSlrsAndWgs_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    pymntstafflts_fndrsngamt = models.BigIntegerField(db_column='PymntsTAfflts_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    pyrlltxs_fndrsngamt = models.BigIntegerField(db_column='PyrllTxs_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    pnsnplncntrbtns_fndrsngamt = models.BigIntegerField(db_column='PnsnPlnCntrbtns_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    pymttrvlentrtnmntpbofcl_fndrsngamt = models.BigIntegerField(db_column='PymtTrvlEntrtnmntPbOfcl_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    rylts_fndrsngamt = models.BigIntegerField(db_column='Rylts_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    ttlfnctnlexpnss_fndrsngamt = models.BigIntegerField(db_column='TtlFnctnlExpnss_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    ttljntcsts_fndrsngamt = models.BigIntegerField(db_column='TtlJntCsts_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    trvl_fndrsngamt = models.BigIntegerField(db_column='Trvl_FndrsngAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_ix'


class ReturnPartV(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtvind = models.CharField(db_column='InfInSkdOPrtVInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    irpdcmntcnt = models.IntegerField(db_column='IRPDcmntCnt', blank=True, null=True)  # Field name made lowercase.
    irpdcmntw2gcnt = models.IntegerField(db_column='IRPDcmntW2GCnt', blank=True, null=True)  # Field name made lowercase.
    bckpwthldcmplncind = models.CharField(db_column='BckpWthldCmplncInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    emplycnt = models.IntegerField(db_column='EmplyCnt', blank=True, null=True)  # Field name made lowercase.
    emplymnttxrtrnsfldind = models.CharField(db_column='EmplymntTxRtrnsFldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unrltdbsincmovrlmtind = models.CharField(db_column='UnrltdBsIncmOvrLmtInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm990tfldind = models.CharField(db_column='Frm990TFldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frgnfnnclaccntind = models.CharField(db_column='FrgnFnnclAccntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prhbtdtxshltrtrnsind = models.CharField(db_column='PrhbtdTxShltrTrnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txblprtyntfctnind = models.CharField(db_column='TxblPrtyNtfctnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm8886tfldind = models.CharField(db_column='Frm8886TFldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    nnddctblcntrbtnsind = models.CharField(db_column='NnddctblCntrbtnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    nnddctblcntrdsclind = models.CharField(db_column='NnddctblCntrDsclInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    qdprqcntrbtnsind = models.CharField(db_column='QdPrQCntrbtnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    qdprqcntrdsclind = models.CharField(db_column='QdPrQCntrDsclInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm8282prprtydspsdofind = models.CharField(db_column='Frm8282PrprtyDspsdOfInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm8282fldcnt = models.IntegerField(db_column='Frm8282FldCnt', blank=True, null=True)  # Field name made lowercase.
    rcvfndstpyprsnlbnftcntrctind = models.CharField(db_column='RcvFndsTPyPrsnlBnftCntrctInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pyprmmsprsnlbnftcntrctind = models.CharField(db_column='PyPrmmsPrsnlBnftCntrctInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm8899fldnd = models.CharField(db_column='Frm8899Fldnd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm1098cfldind = models.CharField(db_column='Frm1098CFldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dafexcssbsnsshldngsind = models.CharField(db_column='DAFExcssBsnssHldngsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txbldstrbtnsind = models.CharField(db_column='TxblDstrbtnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dstrbtntdnrind = models.CharField(db_column='DstrbtnTDnrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    inttnfsandcpcntramt = models.BigIntegerField(db_column='InttnFsAndCpCntrAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsfrpblcusamt = models.BigIntegerField(db_column='GrssRcptsFrPblcUsAmt', blank=True, null=True)  # Field name made lowercase.
    mmbrsandshrgrssincmamt = models.BigIntegerField(db_column='MmbrsAndShrGrssIncmAmt', blank=True, null=True)  # Field name made lowercase.
    othrsrcsgrssincmamt = models.BigIntegerField(db_column='OthrSrcsGrssIncmAmt', blank=True, null=True)  # Field name made lowercase.
    orgfldinloffrm1041ind = models.CharField(db_column='OrgFldInLOfFrm1041Ind', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txexmptintrstamt = models.BigIntegerField(db_column='TxExmptIntrstAmt', blank=True, null=True)  # Field name made lowercase.
    lcnsdmrthnonsttind = models.CharField(db_column='LcnsdMrThnOnSttInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sttrqrdrsrvsamt = models.BigIntegerField(db_column='SttRqrdRsrvsAmt', blank=True, null=True)  # Field name made lowercase.
    rsrvsmntndamt = models.BigIntegerField(db_column='RsrvsMntndAmt', blank=True, null=True)  # Field name made lowercase.
    indrtnnngsrvcsind = models.CharField(db_column='IndrTnnngSrvcsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm720fldind = models.CharField(db_column='Frm720FldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_v'


class ReturnPartVi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtviind = models.CharField(db_column='InfInSkdOPrtVIInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gvrnngbdyvtngmmbrscnt = models.IntegerField(db_column='GvrnngBdyVtngMmbrsCnt', blank=True, null=True)  # Field name made lowercase.
    indpndntvtngmmbrcnt = models.IntegerField(db_column='IndpndntVtngMmbrCnt', blank=True, null=True)  # Field name made lowercase.
    fmlyorbsnssrlnind = models.CharField(db_column='FmlyOrBsnssRlnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dlgtnofmgmtdtsind = models.CharField(db_column='DlgtnOfMgmtDtsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    chngtorgdcmntsind = models.CharField(db_column='ChngTOrgDcmntsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mtrldvrsnormssind = models.CharField(db_column='MtrlDvrsnOrMssInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mmbrsorstckhldrsind = models.CharField(db_column='MmbrsOrStckhldrsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    elctnofbrdmmbrsind = models.CharField(db_column='ElctnOfBrdMmbrsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dcsnssbjcttapprvind = models.CharField(db_column='DcsnsSbjctTApprvInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mntsofgvrnngbdyind = models.CharField(db_column='MntsOfGvrnngBdyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mntsofcmmttsind = models.CharField(db_column='MntsOfCmmttsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    offcrmlngaddrssind = models.CharField(db_column='OffcrMlngAddrssInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lclchptrsind = models.CharField(db_column='LclChptrsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    plcsrfrncchptrsind = models.CharField(db_column='PlcsRfrncChptrsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm990prvddtgvrnbdyind = models.CharField(db_column='Frm990PrvddTGvrnBdyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cnflctofintrstplcyind = models.CharField(db_column='CnflctOfIntrstPlcyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    annldsclsrcvrdprsnind = models.CharField(db_column='AnnlDsclsrCvrdPrsnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rglrmntrngenfrcind = models.CharField(db_column='RglrMntrngEnfrcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    whstlblwrplcyind = models.CharField(db_column='WhstlblwrPlcyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dcmntrtntnplcyind = models.CharField(db_column='DcmntRtntnPlcyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cmpnstnprcssceoind = models.CharField(db_column='CmpnstnPrcssCEOInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cmpnstnprcssothrind = models.CharField(db_column='CmpnstnPrcssOthrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    invstmntinjntvntrind = models.CharField(db_column='InvstmntInJntVntrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wrttnplcyorprcdrind = models.CharField(db_column='WrttnPlcyOrPrcdrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ownwbstind = models.CharField(db_column='OwnWbstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othrwbstind = models.CharField(db_column='OthrWbstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    upnrqstind = models.CharField(db_column='UpnRqstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othrind = models.CharField(db_column='OthrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bksincrofdtl = models.TextField(db_column='BksInCrOfDtl', blank=True, null=True)  # Field name made lowercase.
    bksincrofdtl_prsnnm = models.CharField(db_column='BksInCrOfDtl_PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln1txt = models.CharField(db_column='BsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln2txt = models.CharField(db_column='BsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    bksincrofdtl_phnnm = models.CharField(db_column='BksInCrOfDtl_PhnNm', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_vi'


class ReturnPartVii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtviiind = models.CharField(db_column='InfInSkdOPrtVIIInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nlstdprsnscmpnstdind = models.CharField(db_column='NLstdPrsnsCmpnstdInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ttlrprtblcmpfrmorgamt = models.BigIntegerField(db_column='TtlRprtblCmpFrmOrgAmt', blank=True, null=True)  # Field name made lowercase.
    ttrprtblcmprltdorgamt = models.BigIntegerField(db_column='TtRprtblCmpRltdOrgAmt', blank=True, null=True)  # Field name made lowercase.
    ttlothrcmpnstnamt = models.BigIntegerField(db_column='TtlOthrCmpnstnAmt', blank=True, null=True)  # Field name made lowercase.
    indvrcvdgrtrthn100kcnt = models.IntegerField(db_column='IndvRcvdGrtrThn100KCnt', blank=True, null=True)  # Field name made lowercase.
    frmrofcremplyslstdind = models.CharField(db_column='FrmrOfcrEmplysLstdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ttlcmpgrtrthn150kind = models.CharField(db_column='TtlCmpGrtrThn150KInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cmpnstnfrmothrsrcsind = models.CharField(db_column='CmpnstnFrmOthrSrcsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cntrctrcvdgrtrthn100kcnt = models.IntegerField(db_column='CntrctRcvdGrtrThn100KCnt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_vii'


class ReturnPartViii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtviiiind = models.CharField(db_column='InfInSkdOPrtVIIIInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fdrtdcmpgnsamt = models.BigIntegerField(db_column='FdrtdCmpgnsAmt', blank=True, null=True)  # Field name made lowercase.
    mmbrshpdsamt = models.BigIntegerField(db_column='MmbrshpDsAmt', blank=True, null=True)  # Field name made lowercase.
    fndrsngamt = models.BigIntegerField(db_column='FndrsngAmt', blank=True, null=True)  # Field name made lowercase.
    rltdorgnztnsamt = models.BigIntegerField(db_column='RltdOrgnztnsAmt', blank=True, null=True)  # Field name made lowercase.
    gvrnmntgrntsamt = models.BigIntegerField(db_column='GvrnmntGrntsAmt', blank=True, null=True)  # Field name made lowercase.
    allothrcntrbtnsamt = models.BigIntegerField(db_column='AllOthrCntrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    nncshcntrbtnsamt = models.BigIntegerField(db_column='NncshCntrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlcntrbtnsamt = models.BigIntegerField(db_column='TtlCntrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlprgrmsrvcrvnamt = models.BigIntegerField(db_column='TtlPrgrmSrvcRvnAmt', blank=True, null=True)  # Field name made lowercase.
    grssrnts_rlamt = models.BigIntegerField(db_column='GrssRnts_RlAmt', blank=True, null=True)  # Field name made lowercase.
    grssrnts_prsnlamt = models.BigIntegerField(db_column='GrssRnts_PrsnlAmt', blank=True, null=True)  # Field name made lowercase.
    lssrntlexpnss_rlamt = models.BigIntegerField(db_column='LssRntlExpnss_RlAmt', blank=True, null=True)  # Field name made lowercase.
    lssrntlexpnss_prsnlamt = models.BigIntegerField(db_column='LssRntlExpnss_PrsnlAmt', blank=True, null=True)  # Field name made lowercase.
    rntlincmorlss_rlamt = models.BigIntegerField(db_column='RntlIncmOrLss_RlAmt', blank=True, null=True)  # Field name made lowercase.
    rntlincmorlss_prsnlamt = models.BigIntegerField(db_column='RntlIncmOrLss_PrsnlAmt', blank=True, null=True)  # Field name made lowercase.
    grssamntslsassts_scrtsamt = models.BigIntegerField(db_column='GrssAmntSlsAssts_ScrtsAmt', blank=True, null=True)  # Field name made lowercase.
    grssamntslsassts_othramt = models.BigIntegerField(db_column='GrssAmntSlsAssts_OthrAmt', blank=True, null=True)  # Field name made lowercase.
    lsscstothbssslsexpnss_scrtsamt = models.BigIntegerField(db_column='LssCstOthBssSlsExpnss_ScrtsAmt', blank=True, null=True)  # Field name made lowercase.
    lsscstothbssslsexpnss_othramt = models.BigIntegerField(db_column='LssCstOthBssSlsExpnss_OthrAmt', blank=True, null=True)  # Field name made lowercase.
    gnorlss_scrtsamt = models.BigIntegerField(db_column='GnOrLss_ScrtsAmt', blank=True, null=True)  # Field name made lowercase.
    gnorlss_othramt = models.BigIntegerField(db_column='GnOrLss_OthrAmt', blank=True, null=True)  # Field name made lowercase.
    fndrsnggrssincmamt = models.BigIntegerField(db_column='FndrsngGrssIncmAmt', blank=True, null=True)  # Field name made lowercase.
    cntrrptfndrsngevntamt = models.BigIntegerField(db_column='CntrRptFndrsngEvntAmt', blank=True, null=True)  # Field name made lowercase.
    fndrsngdrctexpnssamt = models.BigIntegerField(db_column='FndrsngDrctExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmfndrsngevt_ttlrvnclmnamt = models.BigIntegerField(db_column='NtIncmFrmFndrsngEvt_TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmfndrsngevt_unrltdbsnssrvnamt = models.BigIntegerField(db_column='NtIncmFrmFndrsngEvt_UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmfndrsngevt_exclsnamt = models.BigIntegerField(db_column='NtIncmFrmFndrsngEvt_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    gmnggrssincmamt = models.BigIntegerField(db_column='GmngGrssIncmAmt', blank=True, null=True)  # Field name made lowercase.
    gmngdrctexpnssamt = models.BigIntegerField(db_column='GmngDrctExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    grssslsofinvntryamt = models.BigIntegerField(db_column='GrssSlsOfInvntryAmt', blank=True, null=True)  # Field name made lowercase.
    cstofgdssldamt = models.BigIntegerField(db_column='CstOfGdsSldAmt', blank=True, null=True)  # Field name made lowercase.
    othrrvnttlamt = models.BigIntegerField(db_column='OthrRvnTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlrvn_ttlrvnclmnamt = models.BigIntegerField(db_column='TtlRvn_TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    ttlrvn_rltdorexmptfncincmamt = models.BigIntegerField(db_column='TtlRvn_RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ttlrvn_unrltdbsnssrvnamt = models.BigIntegerField(db_column='TtlRvn_UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ttlrvn_exclsnamt = models.BigIntegerField(db_column='TtlRvn_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    incmfrminvstbndprcds_ttlrvnclmnamt = models.BigIntegerField(db_column='IncmFrmInvstBndPrcds_TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincm_ttlrvnclmnamt = models.BigIntegerField(db_column='InvstmntIncm_TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    mscrvn_ttlrvnclmnamt = models.BigIntegerField(db_column='MscRvn_TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    ntgnorlssinvstmnts_ttlrvnclmnamt = models.BigIntegerField(db_column='NtGnOrLssInvstmnts_TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmgmng_ttlrvnclmnamt = models.BigIntegerField(db_column='NtIncmFrmGmng_TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmorlss_ttlrvnclmnamt = models.BigIntegerField(db_column='NtIncmOrLss_TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmorlss_ttlrvnclmnamt = models.BigIntegerField(db_column='NtRntlIncmOrLss_TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    ryltsrvn_ttlrvnclmnamt = models.BigIntegerField(db_column='RyltsRvn_TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    ttlothprgrmsrvcrv_ttlrvnclmnamt = models.BigIntegerField(db_column='TtlOthPrgrmSrvcRv_TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    incmfrminvstbndprcds_rltdorexmptfncincmamt = models.BigIntegerField(db_column='IncmFrmInvstBndPrcds_RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincm_rltdorexmptfncincmamt = models.BigIntegerField(db_column='InvstmntIncm_RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    mscrvn_rltdorexmptfncincmamt = models.BigIntegerField(db_column='MscRvn_RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntgnorlssinvstmnts_rltdorexmptfncincmamt = models.BigIntegerField(db_column='NtGnOrLssInvstmnts_RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmgmng_rltdorexmptfncincmamt = models.BigIntegerField(db_column='NtIncmFrmGmng_RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmorlss_rltdorexmptfncincmamt = models.BigIntegerField(db_column='NtIncmOrLss_RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmorlss_rltdorexmptfncincmamt = models.BigIntegerField(db_column='NtRntlIncmOrLss_RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ryltsrvn_rltdorexmptfncincmamt = models.BigIntegerField(db_column='RyltsRvn_RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ttlothprgrmsrvcrv_rltdorexmptfncincmamt = models.BigIntegerField(db_column='TtlOthPrgrmSrvcRv_RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    incmfrminvstbndprcds_unrltdbsnssrvnamt = models.BigIntegerField(db_column='IncmFrmInvstBndPrcds_UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincm_unrltdbsnssrvnamt = models.BigIntegerField(db_column='InvstmntIncm_UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    mscrvn_unrltdbsnssrvnamt = models.BigIntegerField(db_column='MscRvn_UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ntgnorlssinvstmnts_unrltdbsnssrvnamt = models.BigIntegerField(db_column='NtGnOrLssInvstmnts_UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmgmng_unrltdbsnssrvnamt = models.BigIntegerField(db_column='NtIncmFrmGmng_UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmorlss_unrltdbsnssrvnamt = models.BigIntegerField(db_column='NtIncmOrLss_UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmorlss_unrltdbsnssrvnamt = models.BigIntegerField(db_column='NtRntlIncmOrLss_UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ryltsrvn_unrltdbsnssrvnamt = models.BigIntegerField(db_column='RyltsRvn_UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ttlothprgrmsrvcrv_unrltdbsnssrvnamt = models.BigIntegerField(db_column='TtlOthPrgrmSrvcRv_UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    incmfrminvstbndprcds_exclsnamt = models.BigIntegerField(db_column='IncmFrmInvstBndPrcds_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincm_exclsnamt = models.BigIntegerField(db_column='InvstmntIncm_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    mscrvn_exclsnamt = models.BigIntegerField(db_column='MscRvn_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    ntgnorlssinvstmnts_exclsnamt = models.BigIntegerField(db_column='NtGnOrLssInvstmnts_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmgmng_exclsnamt = models.BigIntegerField(db_column='NtIncmFrmGmng_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmorlss_exclsnamt = models.BigIntegerField(db_column='NtIncmOrLss_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmorlss_exclsnamt = models.BigIntegerField(db_column='NtRntlIncmOrLss_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    ryltsrvn_exclsnamt = models.BigIntegerField(db_column='RyltsRvn_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    ttlothprgrmsrvcrv_exclsnamt = models.BigIntegerField(db_column='TtlOthPrgrmSrvcRv_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_viii'


class ReturnPartX(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtxind = models.CharField(db_column='InfInSkdOPrtXInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cshnnintrstbrng_boyamt = models.BigIntegerField(db_column='CshNnIntrstBrng_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    cshnnintrstbrng_eoyamt = models.BigIntegerField(db_column='CshNnIntrstBrng_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    svngsandtmpcshinvst_boyamt = models.BigIntegerField(db_column='SvngsAndTmpCshInvst_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    svngsandtmpcshinvst_eoyamt = models.BigIntegerField(db_column='SvngsAndTmpCshInvst_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    pldgsandgrntsrcvbl_boyamt = models.BigIntegerField(db_column='PldgsAndGrntsRcvbl_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    pldgsandgrntsrcvbl_eoyamt = models.BigIntegerField(db_column='PldgsAndGrntsRcvbl_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    accntsrcvbl_boyamt = models.BigIntegerField(db_column='AccntsRcvbl_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    accntsrcvbl_eoyamt = models.BigIntegerField(db_column='AccntsRcvbl_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    rcvblsfrmoffcrsetc_boyamt = models.BigIntegerField(db_column='RcvblsFrmOffcrsEtc_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    rcvblsfrmoffcrsetc_eoyamt = models.BigIntegerField(db_column='RcvblsFrmOffcrsEtc_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    rcvblfrmdsqlfdprsn_boyamt = models.BigIntegerField(db_column='RcvblFrmDsqlfdPrsn_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    rcvblfrmdsqlfdprsn_eoyamt = models.BigIntegerField(db_column='RcvblFrmDsqlfdPrsn_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    othntslnsrcvblnt_boyamt = models.BigIntegerField(db_column='OthNtsLnsRcvblNt_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    othntslnsrcvblnt_eoyamt = models.BigIntegerField(db_column='OthNtsLnsRcvblNt_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    invntrsfrslorus_boyamt = models.BigIntegerField(db_column='InvntrsFrSlOrUs_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    invntrsfrslorus_eoyamt = models.BigIntegerField(db_column='InvntrsFrSlOrUs_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    prpdexpnssdfrdchrgs_boyamt = models.BigIntegerField(db_column='PrpdExpnssDfrdChrgs_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    prpdexpnssdfrdchrgs_eoyamt = models.BigIntegerField(db_column='PrpdExpnssDfrdChrgs_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    lndbldgeqpcstorothrbssamt = models.BigIntegerField(db_column='LndBldgEqpCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    lndbldgeqpaccmdprcamt = models.BigIntegerField(db_column='LndBldgEqpAccmDprcAmt', blank=True, null=True)  # Field name made lowercase.
    lndbldgeqpbssnt_boyamt = models.BigIntegerField(db_column='LndBldgEqpBssNt_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    lndbldgeqpbssnt_eoyamt = models.BigIntegerField(db_column='LndBldgEqpBssNt_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntspbtrddsc_boyamt = models.BigIntegerField(db_column='InvstmntsPbTrddSc_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntspbtrddsc_eoyamt = models.BigIntegerField(db_column='InvstmntsPbTrddSc_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntsothrscrts_boyamt = models.BigIntegerField(db_column='InvstmntsOthrScrts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntsothrscrts_eoyamt = models.BigIntegerField(db_column='InvstmntsOthrScrts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntsprgrmrltd_boyamt = models.BigIntegerField(db_column='InvstmntsPrgrmRltd_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntsprgrmrltd_eoyamt = models.BigIntegerField(db_column='InvstmntsPrgrmRltd_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    intngblassts_boyamt = models.BigIntegerField(db_column='IntngblAssts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    intngblassts_eoyamt = models.BigIntegerField(db_column='IntngblAssts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrasststtl_boyamt = models.BigIntegerField(db_column='OthrAsstsTtl_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrasststtl_eoyamt = models.BigIntegerField(db_column='OthrAsstsTtl_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttlassts_boyamt = models.BigIntegerField(db_column='TtlAssts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttlassts_eoyamt = models.BigIntegerField(db_column='TtlAssts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    accntspyblaccrexpnss_boyamt = models.BigIntegerField(db_column='AccntsPyblAccrExpnss_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    accntspyblaccrexpnss_eoyamt = models.BigIntegerField(db_column='AccntsPyblAccrExpnss_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    grntspybl_boyamt = models.BigIntegerField(db_column='GrntsPybl_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    grntspybl_eoyamt = models.BigIntegerField(db_column='GrntsPybl_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    dfrrdrvn_boyamt = models.BigIntegerField(db_column='DfrrdRvn_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    dfrrdrvn_eoyamt = models.BigIntegerField(db_column='DfrrdRvn_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    txexmptbndlblts_boyamt = models.BigIntegerField(db_column='TxExmptBndLblts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    txexmptbndlblts_eoyamt = models.BigIntegerField(db_column='TxExmptBndLblts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    escrwaccntlblty_boyamt = models.BigIntegerField(db_column='EscrwAccntLblty_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    escrwaccntlblty_eoyamt = models.BigIntegerField(db_column='EscrwAccntLblty_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    lnsfrmoffcrsdrctrs_boyamt = models.BigIntegerField(db_column='LnsFrmOffcrsDrctrs_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    lnsfrmoffcrsdrctrs_eoyamt = models.BigIntegerField(db_column='LnsFrmOffcrsDrctrs_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    mrtgntspyblscrdinvstprp_boyamt = models.BigIntegerField(db_column='MrtgNtsPyblScrdInvstPrp_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    mrtgntspyblscrdinvstprp_eoyamt = models.BigIntegerField(db_column='MrtgNtsPyblScrdInvstPrp_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    unscrdntslnspybl_boyamt = models.BigIntegerField(db_column='UnscrdNtsLnsPybl_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    unscrdntslnspybl_eoyamt = models.BigIntegerField(db_column='UnscrdNtsLnsPybl_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrlblts_boyamt = models.BigIntegerField(db_column='OthrLblts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrlblts_eoyamt = models.BigIntegerField(db_column='OthrLblts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttllblts_boyamt = models.BigIntegerField(db_column='TtlLblts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttllblts_eoyamt = models.BigIntegerField(db_column='TtlLblts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    orgnztnfllwssfas117ind = models.CharField(db_column='OrgnztnFllwsSFAS117Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unrstrctdntassts_boyamt = models.BigIntegerField(db_column='UnrstrctdNtAssts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    unrstrctdntassts_eoyamt = models.BigIntegerField(db_column='UnrstrctdNtAssts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    tmprrlyrstrntassts_boyamt = models.BigIntegerField(db_column='TmprrlyRstrNtAssts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    tmprrlyrstrntassts_eoyamt = models.BigIntegerField(db_column='TmprrlyRstrNtAssts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    prmnntlyrstrntassts_boyamt = models.BigIntegerField(db_column='PrmnntlyRstrNtAssts_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    prmnntlyrstrntassts_eoyamt = models.BigIntegerField(db_column='PrmnntlyRstrNtAssts_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    orgdsntfllwsfas117ind = models.CharField(db_column='OrgDsNtFllwSFAS117Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cpstktrprncrrntfnds_boyamt = models.BigIntegerField(db_column='CpStkTrPrnCrrntFnds_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    cpstktrprncrrntfnds_eoyamt = models.BigIntegerField(db_column='CpStkTrPrnCrrntFnds_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    pdincpsrplslndbldgeqpfnd_boyamt = models.BigIntegerField(db_column='PdInCpSrplsLndBldgEqpFnd_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    pdincpsrplslndbldgeqpfnd_eoyamt = models.BigIntegerField(db_column='PdInCpSrplsLndBldgEqpFnd_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    rtnernendwmntincmothfnds_boyamt = models.BigIntegerField(db_column='RtnErnEndwmntIncmOthFnds_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    rtnernendwmntincmothfnds_eoyamt = models.BigIntegerField(db_column='RtnErnEndwmntIncmOthFnds_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttlntasstsfndblnc_boyamt = models.BigIntegerField(db_column='TtlNtAsstsFndBlnc_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttlntasstsfndblnc_eoyamt = models.BigIntegerField(db_column='TtlNtAsstsFndBlnc_EOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttlbntasstsfndblnc_boyamt = models.BigIntegerField(db_column='TtLbNtAsstsFndBlnc_BOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttlbntasstsfndblnc_eoyamt = models.BigIntegerField(db_column='TtLbNtAsstsFndBlnc_EOYAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_x'


class ReturnPartXi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtxiind = models.CharField(db_column='InfInSkdOPrtXIInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rcncltnrvnexpnssamt = models.BigIntegerField(db_column='RcncltnRvnExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    ntunrlzdgnslsssinvstamt = models.BigIntegerField(db_column='NtUnrlzdGnsLsssInvstAmt', blank=True, null=True)  # Field name made lowercase.
    dntdsrvcsandusfcltsamt = models.BigIntegerField(db_column='DntdSrvcsAndUsFcltsAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntexpnsamt = models.BigIntegerField(db_column='InvstmntExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    prrprdadjstmntsamt = models.BigIntegerField(db_column='PrrPrdAdjstmntsAmt', blank=True, null=True)  # Field name made lowercase.
    othrchngsinntasstsamt = models.BigIntegerField(db_column='OthrChngsInNtAsstsAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_xi'


class ReturnPartXii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    infinskdoprtxiiind = models.CharField(db_column='InfInSkdOPrtXIIInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accntntcmplorrvwind = models.CharField(db_column='AccntntCmplOrRvwInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    acctcmplorrvwbss_sprtbssfnclstmtind = models.CharField(db_column='AcctCmplOrRvwBss_SprtBssFnclStmtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    acctcmplorrvwbss_cnsldtdbssfnclstmtind = models.CharField(db_column='AcctCmplOrRvwBss_CnsldtdBssFnclStmtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    acctcmplorrvwbss_cnslandspbssfnclstmtind = models.CharField(db_column='AcctCmplOrRvwBss_CnslAndSpBssFnclStmtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fsadtdind = models.CharField(db_column='FSAdtdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fsadtdbss_sprtbssfnclstmtind = models.CharField(db_column='FSAdtdBss_SprtBssFnclStmtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fsadtdbss_cnsldtdbssfnclstmtind = models.CharField(db_column='FSAdtdBss_CnsldtdBssFnclStmtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fsadtdbss_cnslandspbssfnclstmtind = models.CharField(db_column='FSAdtdBss_CnslAndSpBssFnclStmtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    adtcmmttind = models.CharField(db_column='AdtCmmttInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fdrlgrntadtrqrdind = models.CharField(db_column='FdrlGrntAdtRqrdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fdrlgrntadtprfrmdind = models.CharField(db_column='FdrlGrntAdtPrfrmdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mthdofaccntngcshind = models.CharField(db_column='MthdOfAccntngCshInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mthdofaccntngaccrlind = models.CharField(db_column='MthdOfAccntngAccrlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mthdofaccntngothrind = models.TextField(db_column='MthdOfAccntngOthrInd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_part_xii'


class ReturnPfPart0(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    pfsttstrmsct507b1aind = models.CharField(db_column='PFSttsTrmSct507b1AInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    intlrtrnind = models.CharField(db_column='IntlRtrnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    intlrtrnfrmrpbchrtyind = models.CharField(db_column='IntlRtrnFrmrPbChrtyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fnlrtrnind = models.CharField(db_column='FnlRtrnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    amnddrtrnind = models.CharField(db_column='AmnddRtrnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    addrsschngind = models.CharField(db_column='AddrssChngInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fmvasstseoyamt = models.BigIntegerField(db_column='FMVAsstsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    orgnztn501c3exmptpfind = models.CharField(db_column='Orgnztn501c3ExmptPFInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    orgnztn49471trtdpfind = models.CharField(db_column='Orgnztn49471TrtdPFInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    orgnztn501c3txblpfind = models.CharField(db_column='Orgnztn501c3TxblPFInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mthdofaccntngcshind = models.CharField(db_column='MthdOfAccntngCshInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mthdofaccntngaccrlind = models.CharField(db_column='MthdOfAccntngAccrlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mthdofaccntngothrind = models.TextField(db_column='MthdOfAccntngOthrInd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_0'


class ReturnPfPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    anlyssofrvnandexpnss = models.TextField(db_column='AnlyssOfRvnAndExpnss', blank=True, null=True)  # Field name made lowercase.
    cntrrcvdrvandexpnssamt = models.BigIntegerField(db_column='CntrRcvdRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    skdbntrqrdind = models.CharField(db_column='SkdBNtRqrdInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    intrstonsvrvandexpnssamt = models.BigIntegerField(db_column='IntrstOnSvRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    intrstonsvntinvstincmamt = models.BigIntegerField(db_column='IntrstOnSvNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    intrstonsvngsadjntincmamt = models.BigIntegerField(db_column='IntrstOnSvngsAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    dvdndsrvandexpnssamt = models.BigIntegerField(db_column='DvdndsRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    dvdndsntinvstincmamt = models.BigIntegerField(db_column='DvdndsNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    dvdndsadjntincmamt = models.BigIntegerField(db_column='DvdndsAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    grssrntsrvandexpnssamt = models.BigIntegerField(db_column='GrssRntsRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    grssrntsntinvstincmamt = models.BigIntegerField(db_column='GrssRntsNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    grssrntsadjntincmamt = models.BigIntegerField(db_column='GrssRntsAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmorlssamt = models.BigIntegerField(db_column='NtRntlIncmOrLssAmt', blank=True, null=True)  # Field name made lowercase.
    ntgnslastrvandexpnssamt = models.TextField(db_column='NtGnSlAstRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    grssslsprcamt = models.BigIntegerField(db_column='GrssSlsPrcAmt', blank=True, null=True)  # Field name made lowercase.
    cpgnntincmntinvstincmamt = models.BigIntegerField(db_column='CpGnNtIncmNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntstcptlgnadjntincmamt = models.BigIntegerField(db_column='NtSTCptlGnAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    incmmdfctnsadjntincmamt = models.BigIntegerField(db_column='IncmMdfctnsAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    grssslslssrtandallwncamt = models.BigIntegerField(db_column='GrssSlsLssRtAndAllwncAmt', blank=True, null=True)  # Field name made lowercase.
    cstofgdssldamt = models.BigIntegerField(db_column='CstOfGdsSldAmt', blank=True, null=True)  # Field name made lowercase.
    grssprftrvandexpnssamt = models.TextField(db_column='GrssPrftRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    grssprftadjntincmamt = models.BigIntegerField(db_column='GrssPrftAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    othrincmrvandexpnssamt = models.TextField(db_column='OthrIncmRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    othrincmntinvstincmamt = models.BigIntegerField(db_column='OthrIncmNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    othrincmadjntincmamt = models.BigIntegerField(db_column='OthrIncmAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ttlrvandexpnssamt = models.BigIntegerField(db_column='TtlRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    ttlntinvstincmamt = models.BigIntegerField(db_column='TtlNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ttladjntincmamt = models.BigIntegerField(db_column='TtlAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    cmpofcrdrtrstrvandexpnssamt = models.BigIntegerField(db_column='CmpOfcrDrTrstRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    cmpofcrdrtrstntinvstincmamt = models.BigIntegerField(db_column='CmpOfcrDrTrstNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    cmpofcrdrtrstadjntincmamt = models.BigIntegerField(db_column='CmpOfcrDrTrstAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    cmpofcrdrtrstdsbrschrtblamt = models.BigIntegerField(db_column='CmpOfcrDrTrstDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    othemplslrswgsrvandexpnssamt = models.BigIntegerField(db_column='OthEmplSlrsWgsRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    othemplslrswgsntinvstincmamt = models.BigIntegerField(db_column='OthEmplSlrsWgsNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    othemplslrswgsadjntincmamt = models.BigIntegerField(db_column='OthEmplSlrsWgsAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    othemplslrswgsdsbrschrtblamt = models.BigIntegerField(db_column='OthEmplSlrsWgsDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    pnsnemplbnftrvandexpnssamt = models.BigIntegerField(db_column='PnsnEmplBnftRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    pnsnemplbnftntinvstincmamt = models.BigIntegerField(db_column='PnsnEmplBnftNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    pnsnemplbnftadjntincmamt = models.BigIntegerField(db_column='PnsnEmplBnftAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    pnsnemplbnftdsbrschrtblamt = models.BigIntegerField(db_column='PnsnEmplBnftDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    lglfsrvandexpnssamt = models.TextField(db_column='LglFsRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    lglfsntinvstincmamt = models.BigIntegerField(db_column='LglFsNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    lglfsadjntincmamt = models.BigIntegerField(db_column='LglFsAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    lglfsdsbrschrtblamt = models.BigIntegerField(db_column='LglFsDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    accntngfsrvandexpnssamt = models.TextField(db_column='AccntngFsRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    accntngfsntinvstincmamt = models.BigIntegerField(db_column='AccntngFsNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    accntngfsadjntincmamt = models.BigIntegerField(db_column='AccntngFsAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    accntngfschrtblprpsamt = models.BigIntegerField(db_column='AccntngFsChrtblPrpsAmt', blank=True, null=True)  # Field name made lowercase.
    othrprffsrvandexpnssamt = models.TextField(db_column='OthrPrfFsRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    othrprffsntinvstincmamt = models.BigIntegerField(db_column='OthrPrfFsNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    othrprffsadjntincmamt = models.BigIntegerField(db_column='OthrPrfFsAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    othrprffsdsbrschrtblamt = models.BigIntegerField(db_column='OthrPrfFsDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    intrstrvandexpnssamt = models.BigIntegerField(db_column='IntrstRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    intrstntinvstincmamt = models.BigIntegerField(db_column='IntrstNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    intrstadjntincmamt = models.BigIntegerField(db_column='IntrstAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    intrstdsbrschrtblamt = models.BigIntegerField(db_column='IntrstDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    txsrvandexpnssamt = models.TextField(db_column='TxsRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    txsntinvstincmamt = models.BigIntegerField(db_column='TxsNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    txsadjntincmamt = models.BigIntegerField(db_column='TxsAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    txsdsbrschrtblamt = models.BigIntegerField(db_column='TxsDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    dprcanddpltnrvandexpnssamt = models.TextField(db_column='DprcAndDpltnRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    dprcanddpltnntinvstincmamt = models.BigIntegerField(db_column='DprcAndDpltnNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    dprcanddpltnadjntincmamt = models.BigIntegerField(db_column='DprcAndDpltnAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    occpncyrvandexpnssamt = models.BigIntegerField(db_column='OccpncyRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    occpncyntinvstincmamt = models.BigIntegerField(db_column='OccpncyNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    occpncyadjntincmamt = models.BigIntegerField(db_column='OccpncyAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    occpncydsbrschrtblamt = models.BigIntegerField(db_column='OccpncyDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    trvcnfmtngrvandexpnssamt = models.BigIntegerField(db_column='TrvCnfMtngRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    trvcnfmtngntinvstincmamt = models.BigIntegerField(db_column='TrvCnfMtngNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    trvcnfmtngadjntincmamt = models.BigIntegerField(db_column='TrvCnfMtngAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    trvcnfmtngdsbrschrtblamt = models.BigIntegerField(db_column='TrvCnfMtngDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    prntngandpbrvandexpnssamt = models.BigIntegerField(db_column='PrntngAndPbRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    prntngandpbntinvstincmamt = models.BigIntegerField(db_column='PrntngAndPbNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    prntngandpbadjntincmamt = models.BigIntegerField(db_column='PrntngAndPbAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    prntngandpbdsbrschrtblamt = models.BigIntegerField(db_column='PrntngAndPbDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    othrexpnssrvandexpnssamt = models.TextField(db_column='OthrExpnssRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    othrexpnssntinvstincmamt = models.BigIntegerField(db_column='OthrExpnssNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    othrexpnssadjntincmamt = models.BigIntegerField(db_column='OthrExpnssAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    othrexpnssdsbrschrtblamt = models.BigIntegerField(db_column='OthrExpnssDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    ttoprexpnssrvandexpnssamt = models.BigIntegerField(db_column='TtOprExpnssRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    ttoprexpnssntinvstincmamt = models.BigIntegerField(db_column='TtOprExpnssNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ttoprexpnssadjntincmamt = models.BigIntegerField(db_column='TtOprExpnssAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ttoprexpnssdsbrschrtblamt = models.BigIntegerField(db_column='TtOprExpnssDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    cntrpdrvandexpnssamt = models.BigIntegerField(db_column='CntrPdRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    cntrpddsbrschrtblamt = models.BigIntegerField(db_column='CntrPdDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    ttlexpnssrvandexpnssamt = models.BigIntegerField(db_column='TtlExpnssRvAndExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    ttlexpnssntinvstincmamt = models.BigIntegerField(db_column='TtlExpnssNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ttlexpnssadjntincmamt = models.BigIntegerField(db_column='TtlExpnssAdjNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ttlexpnssdsbrschrtblamt = models.BigIntegerField(db_column='TtlExpnssDsbrsChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    excssrvnovrexpnssamt = models.BigIntegerField(db_column='ExcssRvnOvrExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    ntinvstmntincmamt = models.BigIntegerField(db_column='NtInvstmntIncmAmt', blank=True, null=True)  # Field name made lowercase.
    adjstdntincmamt = models.BigIntegerField(db_column='AdjstdNtIncmAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_i'


class ReturnPfPartIi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    frm990pfblncshts = models.TextField(db_column='Frm990PFBlncShts', blank=True, null=True)  # Field name made lowercase.
    cshboyamt = models.BigIntegerField(db_column='CshBOYAmt', blank=True, null=True)  # Field name made lowercase.
    csheoyamt = models.BigIntegerField(db_column='CshEOYAmt', blank=True, null=True)  # Field name made lowercase.
    csheoyfmvamt = models.BigIntegerField(db_column='CshEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    svandtmpcshinvstboyamt = models.BigIntegerField(db_column='SvAndTmpCshInvstBOYAmt', blank=True, null=True)  # Field name made lowercase.
    svandtmpcshinvsteoyamt = models.BigIntegerField(db_column='SvAndTmpCshInvstEOYAmt', blank=True, null=True)  # Field name made lowercase.
    svandtmpcshinvsteoyfmvamt = models.BigIntegerField(db_column='SvAndTmpCshInvstEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    acctrcvblamt = models.BigIntegerField(db_column='AcctRcvblAmt', blank=True, null=True)  # Field name made lowercase.
    acctrcvblallwncdbtflacctamt = models.BigIntegerField(db_column='AcctRcvblAllwncDbtflAcctAmt', blank=True, null=True)  # Field name made lowercase.
    acctrcvblboyamt = models.BigIntegerField(db_column='AcctRcvblBOYAmt', blank=True, null=True)  # Field name made lowercase.
    acctrcvbleoyamt = models.BigIntegerField(db_column='AcctRcvblEOYAmt', blank=True, null=True)  # Field name made lowercase.
    acctrcvbleoyfmvamt = models.BigIntegerField(db_column='AcctRcvblEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    pldgsrcvblamt = models.BigIntegerField(db_column='PldgsRcvblAmt', blank=True, null=True)  # Field name made lowercase.
    pldgsrcvblallwncdbtflacctamt = models.BigIntegerField(db_column='PldgsRcvblAllwncDbtflAcctAmt', blank=True, null=True)  # Field name made lowercase.
    pldgsrcvblboyamt = models.BigIntegerField(db_column='PldgsRcvblBOYAmt', blank=True, null=True)  # Field name made lowercase.
    pldgsrcvbleoyamt = models.BigIntegerField(db_column='PldgsRcvblEOYAmt', blank=True, null=True)  # Field name made lowercase.
    pldgsrcvbleoyfmvamt = models.BigIntegerField(db_column='PldgsRcvblEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    grntsrcvblboyamt = models.BigIntegerField(db_column='GrntsRcvblBOYAmt', blank=True, null=True)  # Field name made lowercase.
    grntsrcvbleoyamt = models.BigIntegerField(db_column='GrntsRcvblEOYAmt', blank=True, null=True)  # Field name made lowercase.
    grntsrcvbleoyfmvamt = models.BigIntegerField(db_column='GrntsRcvblEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    rcvblfrmoffcrsboyamt = models.BigIntegerField(db_column='RcvblFrmOffcrsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    rcvblfrmoffcrseoyamt = models.TextField(db_column='RcvblFrmOffcrsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    rcvblfrmoffcrseoyfmvamt = models.BigIntegerField(db_column='RcvblFrmOffcrsEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    othrntsandlnsrcvblamt = models.BigIntegerField(db_column='OthrNtsAndLnsRcvblAmt', blank=True, null=True)  # Field name made lowercase.
    othrrcvblallwncdbtflacctamt = models.BigIntegerField(db_column='OthrRcvblAllwncDbtflAcctAmt', blank=True, null=True)  # Field name made lowercase.
    othrntsandlnsrcvblboyamt = models.BigIntegerField(db_column='OthrNtsAndLnsRcvblBOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrntsandlnsrcvbleoyamt = models.TextField(db_column='OthrNtsAndLnsRcvblEOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrntsandlnsrcvbleoyfmvamt = models.BigIntegerField(db_column='OthrNtsAndLnsRcvblEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    invntrsboyamt = models.BigIntegerField(db_column='InvntrsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    invntrseoyamt = models.BigIntegerField(db_column='InvntrsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    invntrseoyfmvamt = models.BigIntegerField(db_column='InvntrsEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    prpdexpnssboyamt = models.BigIntegerField(db_column='PrpdExpnssBOYAmt', blank=True, null=True)  # Field name made lowercase.
    prpdexpnsseoyamt = models.BigIntegerField(db_column='PrpdExpnssEOYAmt', blank=True, null=True)  # Field name made lowercase.
    prpdexpnsseoyfmvamt = models.BigIntegerField(db_column='PrpdExpnssEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    usgvrnmntoblgtnsboyamt = models.BigIntegerField(db_column='USGvrnmntOblgtnsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    usgvrnmntoblgtnseoyamt = models.TextField(db_column='USGvrnmntOblgtnsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    usgvtoblgtnseoyfmvamt = models.BigIntegerField(db_column='USGvtOblgtnsEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    crprtstckboyamt = models.BigIntegerField(db_column='CrprtStckBOYAmt', blank=True, null=True)  # Field name made lowercase.
    crprtstckeoyamt = models.TextField(db_column='CrprtStckEOYAmt', blank=True, null=True)  # Field name made lowercase.
    crprtstckeoyfmvamt = models.BigIntegerField(db_column='CrprtStckEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    crprtbndsboyamt = models.BigIntegerField(db_column='CrprtBndsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    crprtbndseoyamt = models.TextField(db_column='CrprtBndsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    crprtbndseoyfmvamt = models.BigIntegerField(db_column='CrprtBndsEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    invstlndcstorothrbssamt = models.BigIntegerField(db_column='InvstLndCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    invstlndaccmdprctnamt = models.BigIntegerField(db_column='InvstLndAccmDprctnAmt', blank=True, null=True)  # Field name made lowercase.
    lndbldginvstmntsboyamt = models.BigIntegerField(db_column='LndBldgInvstmntsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    lndbldginvstmntseoyamt = models.TextField(db_column='LndBldgInvstmntsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    lndbldginvstmntseoyfmvamt = models.BigIntegerField(db_column='LndBldgInvstmntsEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    mrtgglnsboyamt = models.BigIntegerField(db_column='MrtggLnsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    mrtgglnseoyamt = models.BigIntegerField(db_column='MrtggLnsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    mrtgglnseoyfmvamt = models.BigIntegerField(db_column='MrtggLnsEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    othrinvstmntsboyamt = models.BigIntegerField(db_column='OthrInvstmntsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrinvstmntseoyamt = models.TextField(db_column='OthrInvstmntsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrinvstmntseoyfmvamt = models.BigIntegerField(db_column='OthrInvstmntsEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    lndbldgeqpcstorothrbssamt = models.BigIntegerField(db_column='LndBldgEqpCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    lndbldgeqpaccmdprcamt = models.BigIntegerField(db_column='LndBldgEqpAccmDprcAmt', blank=True, null=True)  # Field name made lowercase.
    lndboyamt = models.BigIntegerField(db_column='LndBOYAmt', blank=True, null=True)  # Field name made lowercase.
    lndeoyamt = models.TextField(db_column='LndEOYAmt', blank=True, null=True)  # Field name made lowercase.
    lndeoyfmvamt = models.BigIntegerField(db_column='LndEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    othrasstsboyamt = models.TextField(db_column='OthrAsstsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrasstseoyamt = models.TextField(db_column='OthrAsstsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrasstseoyfmvamt = models.TextField(db_column='OthrAsstsEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    ttlasstsboyamt = models.BigIntegerField(db_column='TtlAsstsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttlasstseoyamt = models.BigIntegerField(db_column='TtlAsstsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttlasstseoyfmvamt = models.BigIntegerField(db_column='TtlAsstsEOYFMVAmt', blank=True, null=True)  # Field name made lowercase.
    accntspyblboyamt = models.BigIntegerField(db_column='AccntsPyblBOYAmt', blank=True, null=True)  # Field name made lowercase.
    accntspybleoyamt = models.BigIntegerField(db_column='AccntsPyblEOYAmt', blank=True, null=True)  # Field name made lowercase.
    grntspyblboyamt = models.BigIntegerField(db_column='GrntsPyblBOYAmt', blank=True, null=True)  # Field name made lowercase.
    grntspybleoyamt = models.BigIntegerField(db_column='GrntsPyblEOYAmt', blank=True, null=True)  # Field name made lowercase.
    dfrrdrvnboyamt = models.BigIntegerField(db_column='DfrrdRvnBOYAmt', blank=True, null=True)  # Field name made lowercase.
    dfrrdrvneoyamt = models.BigIntegerField(db_column='DfrrdRvnEOYAmt', blank=True, null=True)  # Field name made lowercase.
    lnsfrmoffcrsboyamt = models.BigIntegerField(db_column='LnsFrmOffcrsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    lnsfrmoffcrseoyamt = models.TextField(db_column='LnsFrmOffcrsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    mrtggsandntspyblboyamt = models.BigIntegerField(db_column='MrtggsAndNtsPyblBOYAmt', blank=True, null=True)  # Field name made lowercase.
    mrtggsandntspybleoyamt = models.TextField(db_column='MrtggsAndNtsPyblEOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrlbltsboyamt = models.TextField(db_column='OthrLbltsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    othrlbltseoyamt = models.TextField(db_column='OthrLbltsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttllbltsboyamt = models.BigIntegerField(db_column='TtlLbltsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttllbltseoyamt = models.BigIntegerField(db_column='TtlLbltsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    orgnztnfllwssfas117ind = models.CharField(db_column='OrgnztnFllwsSFAS117Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unrstrctdboyamt = models.BigIntegerField(db_column='UnrstrctdBOYAmt', blank=True, null=True)  # Field name made lowercase.
    unrstrctdeoyamt = models.BigIntegerField(db_column='UnrstrctdEOYAmt', blank=True, null=True)  # Field name made lowercase.
    tmprrlyrstrctdboyamt = models.BigIntegerField(db_column='TmprrlyRstrctdBOYAmt', blank=True, null=True)  # Field name made lowercase.
    tmprrlyrstrctdeoyamt = models.BigIntegerField(db_column='TmprrlyRstrctdEOYAmt', blank=True, null=True)  # Field name made lowercase.
    prmnntlyrstrctdboyamt = models.BigIntegerField(db_column='PrmnntlyRstrctdBOYAmt', blank=True, null=True)  # Field name made lowercase.
    prmnntlyrstrctdeoyamt = models.BigIntegerField(db_column='PrmnntlyRstrctdEOYAmt', blank=True, null=True)  # Field name made lowercase.
    orgdsntfllwsfas117ind = models.CharField(db_column='OrgDsNtFllwSFAS117Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cptlstckboyamt = models.BigIntegerField(db_column='CptlStckBOYAmt', blank=True, null=True)  # Field name made lowercase.
    cptlstckeoyamt = models.BigIntegerField(db_column='CptlStckEOYAmt', blank=True, null=True)  # Field name made lowercase.
    addtnlpdincptlboyamt = models.BigIntegerField(db_column='AddtnlPdInCptlBOYAmt', blank=True, null=True)  # Field name made lowercase.
    addtnlpdincptleoyamt = models.BigIntegerField(db_column='AddtnlPdInCptlEOYAmt', blank=True, null=True)  # Field name made lowercase.
    rtndernngboyamt = models.BigIntegerField(db_column='RtndErnngBOYAmt', blank=True, null=True)  # Field name made lowercase.
    rtndernngeoyamt = models.BigIntegerField(db_column='RtndErnngEOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttntastorfndblncsboyamt = models.BigIntegerField(db_column='TtNtAstOrFndBlncsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttntastorfndblncseoyamt = models.BigIntegerField(db_column='TtNtAstOrFndBlncsEOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttllbltsntastboyamt = models.BigIntegerField(db_column='TtlLbltsNtAstBOYAmt', blank=True, null=True)  # Field name made lowercase.
    ttllbltsntasteoyamt = models.BigIntegerField(db_column='TtlLbltsNtAstEOYAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_ii'


class ReturnPfPartIii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    chginntasstsfndblncs = models.TextField(db_column='ChgInNtAsstsFndBlncs', blank=True, null=True)  # Field name made lowercase.
    ttntastorfndblncsboyamt = models.BigIntegerField(db_column='TtNtAstOrFndBlncsBOYAmt', blank=True, null=True)  # Field name made lowercase.
    excssrvnovrexpnssamt = models.BigIntegerField(db_column='ExcssRvnOvrExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    othrincrssamt = models.TextField(db_column='OthrIncrssAmt', blank=True, null=True)  # Field name made lowercase.
    sbttlamt = models.BigIntegerField(db_column='SbttlAmt', blank=True, null=True)  # Field name made lowercase.
    othrdcrssamt = models.TextField(db_column='OthrDcrssAmt', blank=True, null=True)  # Field name made lowercase.
    ttntastorfndblncseoyamt = models.BigIntegerField(db_column='TtNtAstOrFndBlncsEOYAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_iii'


class ReturnPfPartIv(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    cpgnslsstxinvstincmdtl = models.TextField(db_column='CpGnsLssTxInvstIncmDtl', blank=True, null=True)  # Field name made lowercase.
    cptlgnntincmamt = models.BigIntegerField(db_column='CptlGnNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntshrttrmcptlgnlssamt = models.BigIntegerField(db_column='NtShrtTrmCptlGnLssAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_iv'


class ReturnPfPartIxa(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    smmryofdrctchrtblacty = models.TextField(db_column='SmmryOfDrctChrtblActy', blank=True, null=True)  # Field name made lowercase.
    dscrptn1txt = models.TextField(db_column='Dscrptn1Txt', blank=True, null=True)  # Field name made lowercase.
    expnss1amt = models.BigIntegerField(db_column='Expnss1Amt', blank=True, null=True)  # Field name made lowercase.
    dscrptn2txt = models.TextField(db_column='Dscrptn2Txt', blank=True, null=True)  # Field name made lowercase.
    expnss2amt = models.BigIntegerField(db_column='Expnss2Amt', blank=True, null=True)  # Field name made lowercase.
    dscrptn3txt = models.TextField(db_column='Dscrptn3Txt', blank=True, null=True)  # Field name made lowercase.
    expnss3amt = models.BigIntegerField(db_column='Expnss3Amt', blank=True, null=True)  # Field name made lowercase.
    dscrptn4txt = models.TextField(db_column='Dscrptn4Txt', blank=True, null=True)  # Field name made lowercase.
    expnss4amt = models.BigIntegerField(db_column='Expnss4Amt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_ixa'


class ReturnPfPartIxb(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    smofprgrmrltdinvst = models.TextField(db_column='SmOfPrgrmRltdInvst', blank=True, null=True)  # Field name made lowercase.
    dscrptn1txt = models.TextField(db_column='Dscrptn1Txt', blank=True, null=True)  # Field name made lowercase.
    expnss1amt = models.BigIntegerField(db_column='Expnss1Amt', blank=True, null=True)  # Field name made lowercase.
    dscrptn2txt = models.TextField(db_column='Dscrptn2Txt', blank=True, null=True)  # Field name made lowercase.
    expnss2amt = models.BigIntegerField(db_column='Expnss2Amt', blank=True, null=True)  # Field name made lowercase.
    allothrprgrmrltdinvstttamt = models.TextField(db_column='AllOthrPrgrmRltdInvstTtAmt', blank=True, null=True)  # Field name made lowercase.
    ttlamt = models.BigIntegerField(db_column='TtlAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_ixb'


class ReturnPfPartV(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    qlfyundsct4940rdcdtx = models.TextField(db_column='QlfyUndSct4940RdcdTx', blank=True, null=True)  # Field name made lowercase.
    lblsctn4942txind = models.CharField(db_column='LblSctn4942TxInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    adjstdqlfydstryr1amt = models.BigIntegerField(db_column='AdjstdQlfyDstrYr1Amt', blank=True, null=True)  # Field name made lowercase.
    ntvlnnchrtblasstsyr1amt = models.BigIntegerField(db_column='NtVlNnchrtblAsstsYr1Amt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnyr1rt = models.DecimalField(db_column='DstrbtnYr1Rt', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    adjstdqlfydstryr2amt = models.BigIntegerField(db_column='AdjstdQlfyDstrYr2Amt', blank=True, null=True)  # Field name made lowercase.
    ntvlnnchrtblasstsyr2amt = models.BigIntegerField(db_column='NtVlNnchrtblAsstsYr2Amt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnyr2rt = models.DecimalField(db_column='DstrbtnYr2Rt', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    adjstdqlfydstryr3amt = models.BigIntegerField(db_column='AdjstdQlfyDstrYr3Amt', blank=True, null=True)  # Field name made lowercase.
    ntvlnnchrtblasstsyr3amt = models.BigIntegerField(db_column='NtVlNnchrtblAsstsYr3Amt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnyr3rt = models.DecimalField(db_column='DstrbtnYr3Rt', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    adjstdqlfydstryr4amt = models.BigIntegerField(db_column='AdjstdQlfyDstrYr4Amt', blank=True, null=True)  # Field name made lowercase.
    ntvlnnchrtblasstsyr4amt = models.BigIntegerField(db_column='NtVlNnchrtblAsstsYr4Amt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnyr4rt = models.DecimalField(db_column='DstrbtnYr4Rt', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    adjstdqlfydstryr5amt = models.BigIntegerField(db_column='AdjstdQlfyDstrYr5Amt', blank=True, null=True)  # Field name made lowercase.
    ntvlnnchrtblasstsyr5amt = models.BigIntegerField(db_column='NtVlNnchrtblAsstsYr5Amt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnyr5rt = models.DecimalField(db_column='DstrbtnYr5Rt', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    ttldstrbtnrt = models.DecimalField(db_column='TtlDstrbtnRt', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    avrgdstrbtnrt = models.DecimalField(db_column='AvrgDstrbtnRt', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    ntvlnnchrtblasstsamt = models.BigIntegerField(db_column='NtVlNnchrtblAsstsAmt', blank=True, null=True)  # Field name made lowercase.
    adjntvlnnchrtblasstsamt = models.BigIntegerField(db_column='AdjNtVlNnchrtblAsstsAmt', blank=True, null=True)  # Field name made lowercase.
    ntinvstmntincmpctamt = models.BigIntegerField(db_column='NtInvstmntIncmPctAmt', blank=True, null=True)  # Field name made lowercase.
    adjnnchrtblntinvstincmpctamt = models.BigIntegerField(db_column='AdjNnchrtblNtInvstIncmPctAmt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrbtnsamt = models.BigIntegerField(db_column='QlfyngDstrbtnsAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_v'


class ReturnPfPartVi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    excstxbsdoninvstincm = models.TextField(db_column='ExcsTxBsdOnInvstIncm', blank=True, null=True)  # Field name made lowercase.
    exmptoprtngfndtnsind = models.CharField(db_column='ExmptOprtngFndtnsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rlnglttrdt = models.CharField(db_column='RlngLttrDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    dmstcorgmtngsct4940ind = models.CharField(db_column='DmstcOrgMtngSct4940Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    txundrsctn511amt = models.TextField(db_column='TxUndrSctn511Amt', blank=True, null=True)  # Field name made lowercase.
    sbttlamt = models.BigIntegerField(db_column='SbttlAmt', blank=True, null=True)  # Field name made lowercase.
    sbttlatxamt = models.BigIntegerField(db_column='SbttlATxAmt', blank=True, null=True)  # Field name made lowercase.
    txbsdoninvstmntincmamt = models.BigIntegerField(db_column='TxBsdOnInvstmntIncmAmt', blank=True, null=True)  # Field name made lowercase.
    estmtdplsovpmtincmtxamt = models.BigIntegerField(db_column='EstmtdPlsOvpmtIncmTxAmt', blank=True, null=True)  # Field name made lowercase.
    appldtestxamt = models.BigIntegerField(db_column='AppldTEsTxAmt', blank=True, null=True)  # Field name made lowercase.
    bckpwthhldngwthhldamt = models.BigIntegerField(db_column='BckpWthhldngWthhldAmt', blank=True, null=True)  # Field name made lowercase.
    ttlpymntsandcrdtsamt = models.BigIntegerField(db_column='TtlPymntsAndCrdtsAmt', blank=True, null=True)  # Field name made lowercase.
    frm2220attchdind = models.TextField(db_column='Frm2220AttchdInd', blank=True, null=True)  # Field name made lowercase.
    espnltyamt = models.BigIntegerField(db_column='EsPnltyAmt', blank=True, null=True)  # Field name made lowercase.
    amtcrdtnxtyr = models.BigIntegerField(db_column='AmtCrdtNxtYr', blank=True, null=True)  # Field name made lowercase.
    rfndamt = models.BigIntegerField(db_column='RfndAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincmexcstxamt = models.BigIntegerField(db_column='InvstmntIncmExcsTxAmt', blank=True, null=True)  # Field name made lowercase.
    ntapplcblcd = models.TextField(db_column='NtApplcblCd', blank=True, null=True)  # Field name made lowercase.
    orgnlrtrntxpdamt = models.BigIntegerField(db_column='OrgnlRtrnTxPdAmt', blank=True, null=True)  # Field name made lowercase.
    orgnlrtrnovrpymntamt = models.BigIntegerField(db_column='OrgnlRtrnOvrpymntAmt', blank=True, null=True)  # Field name made lowercase.
    txdamt = models.BigIntegerField(db_column='TxDAmt', blank=True, null=True)  # Field name made lowercase.
    ovrpymntamt = models.BigIntegerField(db_column='OvrpymntAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_vi'


class ReturnPfPartViia(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    pf_sttmntsrgrdngacty = models.TextField(db_column='PF_SttmntsRgrdngActy', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_lgsltvpltclactyind = models.TextField(db_column='SttmntsRgrdngActy_LgsltvPltclActyInd', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_mrthn100spntind = models.CharField(db_column='SttmntsRgrdngActy_MrThn100SpntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_frm1120polfldind = models.CharField(db_column='SttmntsRgrdngActy_Frm1120POLFldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_sctn4955orgnztntxamt = models.BigIntegerField(db_column='SttmntsRgrdngActy_Sctn4955OrgnztnTxAmt', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_sctn4955mngrstxamt = models.BigIntegerField(db_column='SttmntsRgrdngActy_Sctn4955MngrsTxAmt', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_txrmbrsdamt = models.BigIntegerField(db_column='SttmntsRgrdngActy_TxRmbrsdAmt', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_actvtsntprvslyrptind = models.TextField(db_column='SttmntsRgrdngActy_ActvtsNtPrvslyRptInd', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_chngstartclsorbylwsind = models.TextField(db_column='SttmntsRgrdngActy_ChngsTArtclsOrBylwsInd', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_unrltdbsincmovrlmtind = models.CharField(db_column='SttmntsRgrdngActy_UnrltdBsIncmOvrLmtInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_frm990tfldind = models.CharField(db_column='SttmntsRgrdngActy_Frm990TFldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_orgnztndsslvdetcind = models.TextField(db_column='SttmntsRgrdngActy_OrgnztnDsslvdEtcInd', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_sctn508rqrstsfdind = models.CharField(db_column='SttmntsRgrdngActy_Sctn508RqrStsfdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_atlst5000inasstsind = models.CharField(db_column='SttmntsRgrdngActy_AtLst5000InAsstsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_frm990pffldwthattygnind = models.TextField(db_column='SttmntsRgrdngActy_Frm990PFFldWthAttyGnInd', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_prvtoprtngfndtnind = models.CharField(db_column='SttmntsRgrdngActy_PrvtOprtngFndtnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_nwsbstntlcntrbtrsind = models.TextField(db_column='SttmntsRgrdngActy_NwSbstntlCntrbtrsInd', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_owncntrlldenttyind = models.TextField(db_column='SttmntsRgrdngActy_OwnCntrlldEnttyInd', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_dnradvsdfndind = models.CharField(db_column='SttmntsRgrdngActy_DnrAdvsdFndInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_cmplywthpblcinsprqrind = models.CharField(db_column='SttmntsRgrdngActy_CmplyWthPblcInspRqrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_wbstaddrsstxt = models.CharField(db_column='SttmntsRgrdngActy_WbstAddrssTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_phnnm = models.CharField(db_column='SttmntsRgrdngActy_PhnNm', max_length=10, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_nectflnginloffrm1041ind = models.CharField(db_column='SttmntsRgrdngActy_NECTFlngInLOFFrm1041Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_txexmptintrstamt = models.BigIntegerField(db_column='SttmntsRgrdngActy_TxExmptIntrstAmt', blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_frgnaccntsqstnind = models.CharField(db_column='SttmntsRgrdngActy_FrgnAccntsQstnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksnm_bsnssnmln1txt = models.CharField(db_column='PrsnsWthBksNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksnm_bsnssnmln2txt = models.CharField(db_column='PrsnsWthBksNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    sttmntsrgrdngacty_indvdlwthbksnm = models.CharField(db_column='SttmntsRgrdngActy_IndvdlWthBksNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    lctnofbksusaddrss_addrssln1txt = models.CharField(db_column='LctnOfBksUSAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    lctnofbksusaddrss_addrssln2txt = models.CharField(db_column='LctnOfBksUSAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    lctnofbksusaddrss_ctynm = models.CharField(db_column='LctnOfBksUSAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    lctnofbksusaddrss_sttabbrvtncd = models.CharField(db_column='LctnOfBksUSAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    lctnofbksusaddrss_zipcd = models.CharField(db_column='LctnOfBksUSAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    lctnofbksfrgnaddrss_addrssln1txt = models.CharField(db_column='LctnOfBksFrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    lctnofbksfrgnaddrss_addrssln2txt = models.CharField(db_column='LctnOfBksFrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    lctnofbksfrgnaddrss_ctynm = models.TextField(db_column='LctnOfBksFrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    lctnofbksfrgnaddrss_prvncorsttnm = models.TextField(db_column='LctnOfBksFrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    lctnofbksfrgnaddrss_cntrycd = models.CharField(db_column='LctnOfBksFrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    lctnofbksfrgnaddrss_frgnpstlcd = models.TextField(db_column='LctnOfBksFrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_viia'


class ReturnPfPartViib(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    sttmntsrgrdngacty4720 = models.TextField(db_column='SttmntsRgrdngActy4720', blank=True, null=True)  # Field name made lowercase.
    slorexchdsqlfdprsnind = models.CharField(db_column='SlOrExchDsqlfdPrsnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    brrworlnddsqlfdprsnind = models.CharField(db_column='BrrwOrLndDsqlfdPrsnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frngdsdsqlfdprsnind = models.CharField(db_column='FrnGdsDsqlfdPrsnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pycmpdsqlfdprsnind = models.CharField(db_column='PyCmpDsqlfdPrsnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    trnsfrastdsqlfdprsnind = models.CharField(db_column='TrnsfrAstDsqlfdPrsnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pymnttgvrnmntoffclind = models.CharField(db_column='PymntTGvrnmntOffclInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    actsfltqlfyasexcptnsind = models.CharField(db_column='ActsFlTQlfyAsExcptnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rlyngcrrntntcdsstrasstind = models.CharField(db_column='RlyngCrrntNtcDsstrAsstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    uncrrctdprractsind = models.CharField(db_column='UncrrctdPrrActsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    undstrbtdincmpyind = models.CharField(db_column='UndstrbtdIncmPYInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    undstrbtdincmpy1yr = models.IntegerField(db_column='UndstrbtdIncmPY1Yr', blank=True, null=True)  # Field name made lowercase.
    undstrbtdincmpy2yr = models.IntegerField(db_column='UndstrbtdIncmPY2Yr', blank=True, null=True)  # Field name made lowercase.
    undstrbtdincmpy3yr = models.IntegerField(db_column='UndstrbtdIncmPY3Yr', blank=True, null=True)  # Field name made lowercase.
    undstrbtdincmpy4yr = models.IntegerField(db_column='UndstrbtdIncmPY4Yr', blank=True, null=True)  # Field name made lowercase.
    undstrincmsct49422ntappind = models.TextField(db_column='UndstrIncmSct49422NtAppInd', blank=True, null=True)  # Field name made lowercase.
    undstrincmsct49422appyr1yr = models.IntegerField(db_column='UndstrIncmSct49422AppYr1Yr', blank=True, null=True)  # Field name made lowercase.
    undstrincmsct49422appyr2yr = models.IntegerField(db_column='UndstrIncmSct49422AppYr2Yr', blank=True, null=True)  # Field name made lowercase.
    undstrincmsct49422appyr3yr = models.IntegerField(db_column='UndstrIncmSct49422AppYr3Yr', blank=True, null=True)  # Field name made lowercase.
    undstrincmsct49422appyr4yr = models.IntegerField(db_column='UndstrIncmSct49422AppYr4Yr', blank=True, null=True)  # Field name made lowercase.
    bsnsshldngsind = models.CharField(db_column='BsnssHldngsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    excssbsnsshldngsind = models.CharField(db_column='ExcssBsnssHldngsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    jprdyinvstmntsind = models.CharField(db_column='JprdyInvstmntsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    uncrrctdpyjprdyinvstind = models.CharField(db_column='UncrrctdPYJprdyInvstInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    inflnclgsltnind = models.CharField(db_column='InflncLgsltnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    inflncelctnind = models.CharField(db_column='InflncElctnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    grntstindvdlsind = models.CharField(db_column='GrntsTIndvdlsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    grntstorgnztnsind = models.CharField(db_column='GrntsTOrgnztnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    nnchrtblprpsind = models.CharField(db_column='NnchrtblPrpsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    trnsctnsfltqlfyasexcind = models.CharField(db_column='TrnsctnsFlTQlfyAsExcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rlyngcrrntntcdsstrasst1ind = models.CharField(db_column='RlyngCrrntNtcDsstrAsst1Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mntndexpndtrrspnsind = models.TextField(db_column='MntndExpndtrRspnsInd', blank=True, null=True)  # Field name made lowercase.
    rcvfndstpyprsnlbnftcntrctind = models.CharField(db_column='RcvFndsTPyPrsnlBnftCntrctInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pyprmmsprsnlbnftcntrctind = models.CharField(db_column='PyPrmmsPrsnlBnftCntrctInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prhbtdtxshltrtrnsind = models.CharField(db_column='PrhbtdTxShltrTrnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prcdsorntincmind = models.CharField(db_column='PrcdsOrNtIncmInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_viib'


class ReturnPfPartViii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    offcrdrtrstkyemplinf = models.TextField(db_column='OffcrDrTrstKyEmplInf', blank=True, null=True)  # Field name made lowercase.
    othremplypdovr50kcnt = models.TextField(db_column='OthrEmplyPdOvr50kCnt', blank=True, null=True)  # Field name made lowercase.
    cntrctrpdovr50kcnt = models.TextField(db_column='CntrctrPdOvr50kCnt', blank=True, null=True)  # Field name made lowercase.
    cmpofhghstpdemplornonetxt = models.TextField(db_column='CmpOfHghstPdEmplOrNONETxt', blank=True, null=True)  # Field name made lowercase.
    cmpofhghstpdcntrctornonetxt = models.TextField(db_column='CmpOfHghstPdCntrctOrNONETxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_viii'


class ReturnPfPartX(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    mnmminvstmntrtrn = models.TextField(db_column='MnmmInvstmntRtrn', blank=True, null=True)  # Field name made lowercase.
    avrgmnthlyfmvofscamt = models.BigIntegerField(db_column='AvrgMnthlyFMVOfScAmt', blank=True, null=True)  # Field name made lowercase.
    avrgmnthlycshblncsamt = models.BigIntegerField(db_column='AvrgMnthlyCshBlncsAmt', blank=True, null=True)  # Field name made lowercase.
    fmvallothrnnchrtblastamt = models.BigIntegerField(db_column='FMVAllOthrNnchrtblAstAmt', blank=True, null=True)  # Field name made lowercase.
    ttlfmvofunsdasstsamt = models.BigIntegerField(db_column='TtlFMVOfUnsdAsstsAmt', blank=True, null=True)  # Field name made lowercase.
    rdctnclmdamt = models.TextField(db_column='RdctnClmdAmt', blank=True, null=True)  # Field name made lowercase.
    acqstnindbtdnssamt = models.BigIntegerField(db_column='AcqstnIndbtdnssAmt', blank=True, null=True)  # Field name made lowercase.
    adjstdttlfmvofunsdastamt = models.BigIntegerField(db_column='AdjstdTtlFMVOfUnsdAstAmt', blank=True, null=True)  # Field name made lowercase.
    cshdmdchrtblamt = models.TextField(db_column='CshDmdChrtblAmt', blank=True, null=True)  # Field name made lowercase.
    ntvlnnchrtblasstsamt = models.BigIntegerField(db_column='NtVlNnchrtblAsstsAmt', blank=True, null=True)  # Field name made lowercase.
    mnmminvstmntrtrnamt = models.BigIntegerField(db_column='MnmmInvstmntRtrnAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_x'


class ReturnPfPartXi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dstrbtblamnt = models.TextField(db_column='DstrbtblAmnt', blank=True, null=True)  # Field name made lowercase.
    sct4942j3j5fndtnandfrgnorgind = models.CharField(db_column='Sct4942j3j5FndtnAndFrgnOrgInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mnmminvstmntrtrnamt = models.BigIntegerField(db_column='MnmmInvstmntRtrnAmt', blank=True, null=True)  # Field name made lowercase.
    txbsdoninvstmntincmamt = models.BigIntegerField(db_column='TxBsdOnInvstmntIncmAmt', blank=True, null=True)  # Field name made lowercase.
    incmtxamt = models.BigIntegerField(db_column='IncmTxAmt', blank=True, null=True)  # Field name made lowercase.
    ttltxamt = models.BigIntegerField(db_column='TtlTxAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtblbfradjamt = models.BigIntegerField(db_column='DstrbtblBfrAdjAmt', blank=True, null=True)  # Field name made lowercase.
    rcvrsqlfddstramt = models.BigIntegerField(db_column='RcvrsQlfdDstrAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtblbfrddamt = models.BigIntegerField(db_column='DstrbtblBfrDdAmt', blank=True, null=True)  # Field name made lowercase.
    ddctnfrmdstrbtblamt = models.BigIntegerField(db_column='DdctnFrmDstrbtblAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtblasadjstdamt = models.BigIntegerField(db_column='DstrbtblAsAdjstdAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_xi'


class ReturnPfPartXii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    qlfyngdstrprtxii = models.TextField(db_column='QlfyngDstrPrtXII', blank=True, null=True)  # Field name made lowercase.
    expnssandcntrbtnsamt = models.TextField(db_column='ExpnssAndCntrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    prgrmrltdinvstttlamt = models.BigIntegerField(db_column='PrgrmRltdInvstTtlAmt', blank=True, null=True)  # Field name made lowercase.
    chrtblasstsacqspdamt = models.BigIntegerField(db_column='ChrtblAsstsAcqsPdAmt', blank=True, null=True)  # Field name made lowercase.
    stasdstbltytstamt = models.BigIntegerField(db_column='StAsdStbltyTstAmt', blank=True, null=True)  # Field name made lowercase.
    stasdcshdstrtstamt = models.TextField(db_column='StAsdCshDstrTstAmt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrbtnsamt = models.BigIntegerField(db_column='QlfyngDstrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    pctsct4940orgntinvstincmamt = models.BigIntegerField(db_column='PctSct4940OrgNtInvstIncmAmt', blank=True, null=True)  # Field name made lowercase.
    adjstdqlfyngdstramt = models.BigIntegerField(db_column='AdjstdQlfyngDstrAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_xii'


class ReturnPfPartXiii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    undstrbtdincm = models.TextField(db_column='UndstrbtdIncm', blank=True, null=True)  # Field name made lowercase.
    dstrbtblasadjstdamt = models.BigIntegerField(db_column='DstrbtblAsAdjstdAmt', blank=True, null=True)  # Field name made lowercase.
    undstrbtdincmpyamt = models.BigIntegerField(db_column='UndstrbtdIncmPYAmt', blank=True, null=True)  # Field name made lowercase.
    prryr1yr = models.IntegerField(db_column='PrrYr1Yr', blank=True, null=True)  # Field name made lowercase.
    prryr2yr = models.IntegerField(db_column='PrrYr2Yr', blank=True, null=True)  # Field name made lowercase.
    prryr3yr = models.IntegerField(db_column='PrrYr3Yr', blank=True, null=True)  # Field name made lowercase.
    ttlfrprryrsamt = models.BigIntegerField(db_column='TtlFrPrrYrsAmt', blank=True, null=True)  # Field name made lowercase.
    excssdstrbtncyvyr5amt = models.BigIntegerField(db_column='ExcssDstrbtnCyvYr5Amt', blank=True, null=True)  # Field name made lowercase.
    excssdstrbtncyvyr4amt = models.BigIntegerField(db_column='ExcssDstrbtnCyvYr4Amt', blank=True, null=True)  # Field name made lowercase.
    excssdstrbtncyvyr3amt = models.BigIntegerField(db_column='ExcssDstrbtnCyvYr3Amt', blank=True, null=True)  # Field name made lowercase.
    excssdstrbtncyvyr2amt = models.BigIntegerField(db_column='ExcssDstrbtnCyvYr2Amt', blank=True, null=True)  # Field name made lowercase.
    excssdstrbtncyvyr1amt = models.BigIntegerField(db_column='ExcssDstrbtnCyvYr1Amt', blank=True, null=True)  # Field name made lowercase.
    ttlexcssdstrbtncyvamt = models.BigIntegerField(db_column='TtlExcssDstrbtnCyvAmt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrbtnsamt = models.BigIntegerField(db_column='QlfyngDstrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    appldtyr1amt = models.BigIntegerField(db_column='AppldTYr1Amt', blank=True, null=True)  # Field name made lowercase.
    appldtprryrsamt = models.TextField(db_column='AppldTPrrYrsAmt', blank=True, null=True)  # Field name made lowercase.
    trtdasdstrfrmcrpsamt = models.TextField(db_column='TrtdAsDstrFrmCrpsAmt', blank=True, null=True)  # Field name made lowercase.
    appldtcrrntyramt = models.BigIntegerField(db_column='AppldTCrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    rmnngdstrfrmcrpsamt = models.BigIntegerField(db_column='RmnngDstrFrmCrpsAmt', blank=True, null=True)  # Field name made lowercase.
    excssdstrcyvappcycrpsamt = models.BigIntegerField(db_column='ExcssDstrCyvAppCYCrpsAmt', blank=True, null=True)  # Field name made lowercase.
    excssdstrbtncyvappcyamt = models.BigIntegerField(db_column='ExcssDstrbtnCyvAppCYAmt', blank=True, null=True)  # Field name made lowercase.
    ttlcrpsamt = models.BigIntegerField(db_column='TtlCrpsAmt', blank=True, null=True)  # Field name made lowercase.
    prryrundstrbtdincmamt = models.BigIntegerField(db_column='PrrYrUndstrbtdIncmAmt', blank=True, null=True)  # Field name made lowercase.
    prryrdfcncyortxamt = models.BigIntegerField(db_column='PrrYrDfcncyOrTxAmt', blank=True, null=True)  # Field name made lowercase.
    txbl1amt = models.BigIntegerField(db_column='Txbl1Amt', blank=True, null=True)  # Field name made lowercase.
    txbl2amt = models.BigIntegerField(db_column='Txbl2Amt', blank=True, null=True)  # Field name made lowercase.
    undstrbtdincmcyamt = models.BigIntegerField(db_column='UndstrbtdIncmCYAmt', blank=True, null=True)  # Field name made lowercase.
    crpsdstr170b1eor4942g3amt = models.BigIntegerField(db_column='CrpsDstr170b1EOr4942g3Amt', blank=True, null=True)  # Field name made lowercase.
    excssdstrcyvfrmyr5amt = models.BigIntegerField(db_column='ExcssDstrCyvFrmYr5Amt', blank=True, null=True)  # Field name made lowercase.
    excssdstrcyvtnxtyramt = models.BigIntegerField(db_column='ExcssDstrCyvTNxtYrAmt', blank=True, null=True)  # Field name made lowercase.
    excssfrmyr4amt = models.BigIntegerField(db_column='ExcssFrmYr4Amt', blank=True, null=True)  # Field name made lowercase.
    excssfrmyr3amt = models.BigIntegerField(db_column='ExcssFrmYr3Amt', blank=True, null=True)  # Field name made lowercase.
    excssfrmyr2amt = models.BigIntegerField(db_column='ExcssFrmYr2Amt', blank=True, null=True)  # Field name made lowercase.
    excssfrmyr1amt = models.BigIntegerField(db_column='ExcssFrmYr1Amt', blank=True, null=True)  # Field name made lowercase.
    excssfrmcrrntyramt = models.BigIntegerField(db_column='ExcssFrmCrrntYrAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_xiii'


class ReturnPfPartXiv(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    pf_prvtoprtngfndtns = models.TextField(db_column='PF_PrvtOprtngFndtns', blank=True, null=True)  # Field name made lowercase.
    prvtoprtngfndtns_prvtoprtngfndtnrlngdt = models.CharField(db_column='PrvtOprtngFndtns_PrvtOprtngFndtnRlngDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    lssradjntincmmninvstrt_crrntyramt = models.BigIntegerField(db_column='LssrAdjNtIncmMnInvstRt_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    lssradjntincmmninvstrt_yr1amt = models.BigIntegerField(db_column='LssrAdjNtIncmMnInvstRt_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    lssradjntincmmninvstrt_yr2amt = models.BigIntegerField(db_column='LssrAdjNtIncmMnInvstRt_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    lssradjntincmmninvstrt_yr3amt = models.BigIntegerField(db_column='LssrAdjNtIncmMnInvstRt_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    lssradjntincmmninvstrt_ttlamt = models.BigIntegerField(db_column='LssrAdjNtIncmMnInvstRt_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    pct85lssradjincmormnrt_crrntyramt = models.BigIntegerField(db_column='Pct85LssrAdjIncmOrMnRt_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    pct85lssradjincmormnrt_yr1amt = models.BigIntegerField(db_column='Pct85LssrAdjIncmOrMnRt_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    pct85lssradjincmormnrt_yr2amt = models.BigIntegerField(db_column='Pct85LssrAdjIncmOrMnRt_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    pct85lssradjincmormnrt_yr3amt = models.BigIntegerField(db_column='Pct85LssrAdjIncmOrMnRt_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    pct85lssradjincmormnrt_ttlamt = models.BigIntegerField(db_column='Pct85LssrAdjIncmOrMnRt_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrbtns_crrntyramt = models.BigIntegerField(db_column='QlfyngDstrbtns_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrbtns_yr1amt = models.BigIntegerField(db_column='QlfyngDstrbtns_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrbtns_yr2amt = models.BigIntegerField(db_column='QlfyngDstrbtns_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrbtns_yr3amt = models.BigIntegerField(db_column='QlfyngDstrbtns_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrbtns_ttlamt = models.BigIntegerField(db_column='QlfyngDstrbtns_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrntusddrt_crrntyramt = models.BigIntegerField(db_column='QlfyngDstrNtUsdDrt_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrntusddrt_yr1amt = models.BigIntegerField(db_column='QlfyngDstrNtUsdDrt_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrntusddrt_yr2amt = models.BigIntegerField(db_column='QlfyngDstrNtUsdDrt_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrntusddrt_yr3amt = models.BigIntegerField(db_column='QlfyngDstrNtUsdDrt_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrntusddrt_ttlamt = models.BigIntegerField(db_column='QlfyngDstrNtUsdDrt_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrmddrt_crrntyramt = models.BigIntegerField(db_column='QlfyngDstrMdDrt_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrmddrt_yr1amt = models.BigIntegerField(db_column='QlfyngDstrMdDrt_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrmddrt_yr2amt = models.BigIntegerField(db_column='QlfyngDstrMdDrt_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrmddrt_yr3amt = models.BigIntegerField(db_column='QlfyngDstrMdDrt_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    qlfyngdstrmddrt_ttlamt = models.BigIntegerField(db_column='QlfyngDstrMdDrt_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlassts_crrntyramt = models.BigIntegerField(db_column='TtlAssts_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlassts_yr1amt = models.BigIntegerField(db_column='TtlAssts_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    ttlassts_yr2amt = models.BigIntegerField(db_column='TtlAssts_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    ttlassts_yr3amt = models.BigIntegerField(db_column='TtlAssts_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    ttlassts_ttlamt = models.BigIntegerField(db_column='TtlAssts_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlasstssct4942j3b_crrntyramt = models.BigIntegerField(db_column='TtlAsstsSct4942j3B_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlasstssct4942j3b_yr1amt = models.BigIntegerField(db_column='TtlAsstsSct4942j3B_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    ttlasstssct4942j3b_yr2amt = models.BigIntegerField(db_column='TtlAsstsSct4942j3B_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    ttlasstssct4942j3b_yr3amt = models.BigIntegerField(db_column='TtlAsstsSct4942j3B_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    ttlasstssct4942j3b_ttlamt = models.BigIntegerField(db_column='TtlAsstsSct4942j3B_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    twthrdsmnmminvstrt_crrntyramt = models.BigIntegerField(db_column='TwThrdsMnmmInvstRt_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    twthrdsmnmminvstrt_yr1amt = models.BigIntegerField(db_column='TwThrdsMnmmInvstRt_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    twthrdsmnmminvstrt_yr2amt = models.BigIntegerField(db_column='TwThrdsMnmmInvstRt_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    twthrdsmnmminvstrt_yr3amt = models.BigIntegerField(db_column='TwThrdsMnmmInvstRt_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    twthrdsmnmminvstrt_ttlamt = models.BigIntegerField(db_column='TwThrdsMnmmInvstRt_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlspprt_crrntyramt = models.BigIntegerField(db_column='TtlSpprt_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlspprt_yr1amt = models.BigIntegerField(db_column='TtlSpprt_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    ttlspprt_yr2amt = models.BigIntegerField(db_column='TtlSpprt_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    ttlspprt_yr3amt = models.BigIntegerField(db_column='TtlSpprt_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    ttlspprt_ttlamt = models.BigIntegerField(db_column='TtlSpprt_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    pblcspprt_crrntyramt = models.BigIntegerField(db_column='PblcSpprt_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    pblcspprt_yr1amt = models.BigIntegerField(db_column='PblcSpprt_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    pblcspprt_yr2amt = models.BigIntegerField(db_column='PblcSpprt_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    pblcspprt_yr3amt = models.BigIntegerField(db_column='PblcSpprt_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    pblcspprt_ttlamt = models.BigIntegerField(db_column='PblcSpprt_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    lrgstspprtfrmeo_crrntyramt = models.BigIntegerField(db_column='LrgstSpprtFrmEO_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    lrgstspprtfrmeo_yr1amt = models.BigIntegerField(db_column='LrgstSpprtFrmEO_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    lrgstspprtfrmeo_yr2amt = models.BigIntegerField(db_column='LrgstSpprtFrmEO_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    lrgstspprtfrmeo_yr3amt = models.BigIntegerField(db_column='LrgstSpprtFrmEO_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    lrgstspprtfrmeo_ttlamt = models.BigIntegerField(db_column='LrgstSpprtFrmEO_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm_crrntyramt = models.BigIntegerField(db_column='GrssInvstmntIncm_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm_yr1amt = models.BigIntegerField(db_column='GrssInvstmntIncm_Yr1Amt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm_yr2amt = models.BigIntegerField(db_column='GrssInvstmntIncm_Yr2Amt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm_yr3amt = models.BigIntegerField(db_column='GrssInvstmntIncm_Yr3Amt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm_ttlamt = models.BigIntegerField(db_column='GrssInvstmntIncm_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    prvtoprtngfndtns_sctn4942j3ind = models.CharField(db_column='PrvtOprtngFndtns_Sctn4942j3Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prvtoprtngfndtns_sctn4942j5ind = models.CharField(db_column='PrvtOprtngFndtns_Sctn4942j5Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_xiv'


class ReturnPfPartXv(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntryinfrmtn = models.TextField(db_column='SpplmntryInfrmtn', blank=True, null=True)  # Field name made lowercase.
    onlycntrtprslctdind = models.CharField(db_column='OnlyCntrTPrslctdInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ttlgrntorcntrpddryramt = models.BigIntegerField(db_column='TtlGrntOrCntrPdDrYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlgrntorcntrapprvftamt = models.BigIntegerField(db_column='TtlGrntOrCntrApprvFtAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_xv'


class ReturnPfPartXvia(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    pf_anlyssincmprdcngacty = models.TextField(db_column='PF_AnlyssIncmPrdcngActy', blank=True, null=True)  # Field name made lowercase.
    anlyssincmprdcngacty_sbttlsincmprdcngacty = models.TextField(db_column='AnlyssIncmPrdcngActy_SbttlsIncmPrdcngActy', blank=True, null=True)  # Field name made lowercase.
    sbttlsincmprdcngacty_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='SbttlsIncmPrdcngActy_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    sbttlsincmprdcngacty_exclsnamt = models.BigIntegerField(db_column='SbttlsIncmPrdcngActy_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    sbttlsincmprdcngacty_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='SbttlsIncmPrdcngActy_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.
    anlyssincmprdcngacty_ttlincmprdcngactyamt = models.BigIntegerField(db_column='AnlyssIncmPrdcngActy_TtlIncmPrdcngActyAmt', blank=True, null=True)  # Field name made lowercase.
    dvandintfrmscprtvii_bsnsscd = models.TextField(db_column='DvAndIntFrmScPrtVII_BsnssCd', blank=True, null=True)  # Field name made lowercase.
    fscntrctsfrmgvtag_bsnsscd = models.TextField(db_column='FsCntrctsFrmGvtAg_BsnssCd', blank=True, null=True)  # Field name made lowercase.
    gnslsastoththninvntry_bsnsscd = models.TextField(db_column='GnSlsAstOthThnInvntry_BsnssCd', blank=True, null=True)  # Field name made lowercase.
    grssprftlssslsofinvntry_bsnsscd = models.TextField(db_column='GrssPrftLssSlsOfInvntry_BsnssCd', blank=True, null=True)  # Field name made lowercase.
    intonsvandtmpcshinvst_bsnsscd = models.TextField(db_column='IntOnSvAndTmpCshInvst_BsnssCd', blank=True, null=True)  # Field name made lowercase.
    mmbrshpdsandassmnt_bsnsscd = models.TextField(db_column='MmbrshpDsAndAssmnt_BsnssCd', blank=True, null=True)  # Field name made lowercase.
    ntincmlssfrmspclevt_bsnsscd = models.TextField(db_column='NtIncmLssFrmSpclEvt_BsnssCd', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmprsnlprp_bsnsscd = models.TextField(db_column='NtRntlIncmPrsnlPrp_BsnssCd', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmrdbtfncdprp_bsnsscd = models.TextField(db_column='NtRntlIncmRDbtFncdPrp_BsnssCd', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmrntdbtfncdprp_bsnsscd = models.TextField(db_column='NtRntlIncmRNtDbtFncdPrp_BsnssCd', blank=True, null=True)  # Field name made lowercase.
    othrinvstmntincmprtvii_bsnsscd = models.TextField(db_column='OthrInvstmntIncmPrtVII_BsnssCd', blank=True, null=True)  # Field name made lowercase.
    dvandintfrmscprtvii_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='DvAndIntFrmScPrtVII_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    fscntrctsfrmgvtag_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='FsCntrctsFrmGvtAg_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    gnslsastoththninvntry_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='GnSlsAstOthThnInvntry_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    grssprftlssslsofinvntry_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='GrssPrftLssSlsOfInvntry_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    intonsvandtmpcshinvst_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='IntOnSvAndTmpCshInvst_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    mmbrshpdsandassmnt_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='MmbrshpDsAndAssmnt_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmlssfrmspclevt_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='NtIncmLssFrmSpclEvt_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmprsnlprp_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='NtRntlIncmPrsnlPrp_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmrdbtfncdprp_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='NtRntlIncmRDbtFncdPrp_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmrntdbtfncdprp_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='NtRntlIncmRNtDbtFncdPrp_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    othrinvstmntincmprtvii_unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='OthrInvstmntIncmPrtVII_UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    dvandintfrmscprtvii_exclsncd = models.TextField(db_column='DvAndIntFrmScPrtVII_ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    fscntrctsfrmgvtag_exclsncd = models.TextField(db_column='FsCntrctsFrmGvtAg_ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    gnslsastoththninvntry_exclsncd = models.TextField(db_column='GnSlsAstOthThnInvntry_ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    grssprftlssslsofinvntry_exclsncd = models.TextField(db_column='GrssPrftLssSlsOfInvntry_ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    intonsvandtmpcshinvst_exclsncd = models.TextField(db_column='IntOnSvAndTmpCshInvst_ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    mmbrshpdsandassmnt_exclsncd = models.TextField(db_column='MmbrshpDsAndAssmnt_ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    ntincmlssfrmspclevt_exclsncd = models.TextField(db_column='NtIncmLssFrmSpclEvt_ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmprsnlprp_exclsncd = models.TextField(db_column='NtRntlIncmPrsnlPrp_ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmrdbtfncdprp_exclsncd = models.TextField(db_column='NtRntlIncmRDbtFncdPrp_ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmrntdbtfncdprp_exclsncd = models.TextField(db_column='NtRntlIncmRNtDbtFncdPrp_ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    othrinvstmntincmprtvii_exclsncd = models.TextField(db_column='OthrInvstmntIncmPrtVII_ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    dvandintfrmscprtvii_exclsnamt = models.BigIntegerField(db_column='DvAndIntFrmScPrtVII_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    fscntrctsfrmgvtag_exclsnamt = models.BigIntegerField(db_column='FsCntrctsFrmGvtAg_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    gnslsastoththninvntry_exclsnamt = models.BigIntegerField(db_column='GnSlsAstOthThnInvntry_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    grssprftlssslsofinvntry_exclsnamt = models.BigIntegerField(db_column='GrssPrftLssSlsOfInvntry_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    intonsvandtmpcshinvst_exclsnamt = models.BigIntegerField(db_column='IntOnSvAndTmpCshInvst_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    mmbrshpdsandassmnt_exclsnamt = models.BigIntegerField(db_column='MmbrshpDsAndAssmnt_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmlssfrmspclevt_exclsnamt = models.BigIntegerField(db_column='NtIncmLssFrmSpclEvt_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmprsnlprp_exclsnamt = models.BigIntegerField(db_column='NtRntlIncmPrsnlPrp_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmrdbtfncdprp_exclsnamt = models.BigIntegerField(db_column='NtRntlIncmRDbtFncdPrp_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmrntdbtfncdprp_exclsnamt = models.BigIntegerField(db_column='NtRntlIncmRNtDbtFncdPrp_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    othrinvstmntincmprtvii_exclsnamt = models.BigIntegerField(db_column='OthrInvstmntIncmPrtVII_ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    dvandintfrmscprtvii_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='DvAndIntFrmScPrtVII_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.
    fscntrctsfrmgvtag_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='FsCntrctsFrmGvtAg_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.
    gnslsastoththninvntry_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='GnSlsAstOthThnInvntry_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.
    grssprftlssslsofinvntry_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='GrssPrftLssSlsOfInvntry_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.
    intonsvandtmpcshinvst_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='IntOnSvAndTmpCshInvst_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.
    mmbrshpdsandassmnt_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='MmbrshpDsAndAssmnt_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmlssfrmspclevt_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='NtIncmLssFrmSpclEvt_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmprsnlprp_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='NtRntlIncmPrsnlPrp_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmrdbtfncdprp_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='NtRntlIncmRDbtFncdPrp_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.
    ntrntlincmrntdbtfncdprp_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='NtRntlIncmRNtDbtFncdPrp_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.
    othrinvstmntincmprtvii_rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='OthrInvstmntIncmPrtVII_RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_xvia'


class ReturnPfPartXvib(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    rlnofactytaccmofexmptprps = models.TextField(db_column='RlnOfActyTAccmOfExmptPrps', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_xvib'


class ReturnPfPartXvii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    trnsfrtrnsrlnnnchrtbleo = models.TextField(db_column='TrnsfrTrnsRlnNnchrtblEO', blank=True, null=True)  # Field name made lowercase.
    trnsfrofcshtnnchrtbleoind = models.CharField(db_column='TrnsfrOfCshTNnchrtblEOInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    trnsfrothrasstnnchrtbleoind = models.CharField(db_column='TrnsfrOthrAsstNnchrtblEOInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    slsorexchngsofasstsind = models.CharField(db_column='SlsOrExchngsOfAsstsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prchsofasstsnnchrtbleoind = models.CharField(db_column='PrchsOfAsstsNnchrtblEOInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rntloffcltsothasstsind = models.CharField(db_column='RntlOfFcltsOthAsstsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rmbrsmntarrngmntsind = models.CharField(db_column='RmbrsmntArrngmntsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lnsorlngrntsind = models.CharField(db_column='LnsOrLnGrntsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prfrmncofsrvcsetcind = models.CharField(db_column='PrfrmncOfSrvcsEtcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shrngoffcltsetcind = models.CharField(db_column='ShrngOfFcltsEtcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rltnshpsnnchrtbleoind = models.CharField(db_column='RltnshpsNnchrtblEOInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pf_part_xvii'


class ReturnPfapplctnsbmssninf(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntryinfrmtn_applctnsbmssninf = models.TextField(db_column='SpplmntryInfrmtn_ApplctnSbmssnInf', blank=True, null=True)  # Field name made lowercase.
    applctnsbmssninf_rcpntprsnnm = models.CharField(db_column='ApplctnSbmssnInf_RcpntPrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    applctnsbmssninf_rcpntphnnm = models.CharField(db_column='ApplctnSbmssnInf_RcpntPhnNm', max_length=10, blank=True, null=True)  # Field name made lowercase.
    applctnsbmssninf_rcpntemladdrsstxt = models.CharField(db_column='ApplctnSbmssnInf_RcpntEmlAddrssTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    applctnsbmssninf_frmandinfandmtrlstxt = models.TextField(db_column='ApplctnSbmssnInf_FrmAndInfAndMtrlsTxt', blank=True, null=True)  # Field name made lowercase.
    applctnsbmssninf_sbmssnddlnstxt = models.CharField(db_column='ApplctnSbmssnInf_SbmssnDdlnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    applctnsbmssninf_rstrctnsonawrdstxt = models.TextField(db_column='ApplctnSbmssnInf_RstrctnsOnAwrdsTxt', blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_addrssln1txt = models.CharField(db_column='RcpntUSAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_addrssln2txt = models.CharField(db_column='RcpntUSAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_ctynm = models.CharField(db_column='RcpntUSAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_sttabbrvtncd = models.CharField(db_column='RcpntUSAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_zipcd = models.CharField(db_column='RcpntUSAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_addrssln1txt = models.CharField(db_column='RcpntFrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_addrssln2txt = models.CharField(db_column='RcpntFrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_ctynm = models.TextField(db_column='RcpntFrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_cntrycd = models.CharField(db_column='RcpntFrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_frgnpstlcd = models.TextField(db_column='RcpntFrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_prvncorsttnm = models.TextField(db_column='RcpntFrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfapplctnsbmssninf'


class ReturnPfcmpnstnhghstpdempl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    offcrdrtrstkyemplinf_cmpnstnhghstpdempl = models.TextField(db_column='OffcrDrTrstKyEmplInf_CmpnstnHghstPdEmpl', blank=True, null=True)  # Field name made lowercase.
    cmpnstnhghstpdempl_prsnnm = models.TextField(db_column='CmpnstnHghstPdEmpl_PrsnNm', blank=True, null=True)  # Field name made lowercase.
    cmpnstnhghstpdempl_ttltxt = models.CharField(db_column='CmpnstnHghstPdEmpl_TtlTxt', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cmpnstnhghstpdempl_avrghrsprwkdvtdtpsrt = models.TextField(db_column='CmpnstnHghstPdEmpl_AvrgHrsPrWkDvtdTPsRt', blank=True, null=True)  # Field name made lowercase.
    cmpnstnhghstpdempl_cmpnstnamt = models.BigIntegerField(db_column='CmpnstnHghstPdEmpl_CmpnstnAmt', blank=True, null=True)  # Field name made lowercase.
    cmpnstnhghstpdempl_emplybnftsamt = models.BigIntegerField(db_column='CmpnstnHghstPdEmpl_EmplyBnftsAmt', blank=True, null=True)  # Field name made lowercase.
    cmpnstnhghstpdempl_expnsaccntamt = models.BigIntegerField(db_column='CmpnstnHghstPdEmpl_ExpnsAccntAmt', blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfcmpnstnhghstpdempl'


class ReturnPfcmpnstnofhghstpdcntrct(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    offcrdrtrstkyemplinf_cmpnstnofhghstpdcntrct = models.TextField(db_column='OffcrDrTrstKyEmplInf_CmpnstnOfHghstPdCntrct', blank=True, null=True)  # Field name made lowercase.
    cmpnstnofhghstpdcntrct_bsnssnmln1 = models.TextField(db_column='CmpnstnOfHghstPdCntrct_BsnssNmLn1', blank=True, null=True)  # Field name made lowercase.
    cmpnstnofhghstpdcntrct_bsnssnmln2 = models.TextField(db_column='CmpnstnOfHghstPdCntrct_BsnssNmLn2', blank=True, null=True)  # Field name made lowercase.
    cmpnstnofhghstpdcntrct_prsnnm = models.TextField(db_column='CmpnstnOfHghstPdCntrct_PrsnNm', blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    cmpnstnofhghstpdcntrct_srvctxt = models.CharField(db_column='CmpnstnOfHghstPdCntrct_SrvcTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cmpnstnofhghstpdcntrct_cmpnstnamt = models.BigIntegerField(db_column='CmpnstnOfHghstPdCntrct_CmpnstnAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfcmpnstnofhghstpdcntrct'


class ReturnPfcntrbtngmngrnm(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    cntrbtngmngrnm = models.CharField(db_column='CntrbtngMngrNm', max_length=35, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfcntrbtngmngrnm'


class ReturnPfcpgnslsstxinvstincm(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    cpgnslsstxinvstincm = models.TextField(db_column='CpGnsLssTxInvstIncm', blank=True, null=True)  # Field name made lowercase.
    prprtydsc = models.CharField(db_column='PrprtyDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hwacqrdcd = models.TextField(db_column='HwAcqrdCd', blank=True, null=True)  # Field name made lowercase.
    acqrddt = models.CharField(db_column='AcqrdDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    slddt = models.CharField(db_column='SldDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    grssslsprcamt = models.BigIntegerField(db_column='GrssSlsPrcAmt', blank=True, null=True)  # Field name made lowercase.
    dprctnamt = models.BigIntegerField(db_column='DprctnAmt', blank=True, null=True)  # Field name made lowercase.
    cstorothrbssamt = models.BigIntegerField(db_column='CstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    gnorlssamt = models.BigIntegerField(db_column='GnOrLssAmt', blank=True, null=True)  # Field name made lowercase.
    fmvasof123169amt = models.BigIntegerField(db_column='FMVAsOf123169Amt', blank=True, null=True)  # Field name made lowercase.
    adjstdbssasof123169amt = models.BigIntegerField(db_column='AdjstdBssAsOf123169Amt', blank=True, null=True)  # Field name made lowercase.
    excssfmvovradjstdbssamt = models.BigIntegerField(db_column='ExcssFMVOvrAdjstdBssAmt', blank=True, null=True)  # Field name made lowercase.
    gnsmnsexcssorlsssamt = models.BigIntegerField(db_column='GnsMnsExcssOrLsssAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfcpgnslsstxinvstincm'


class ReturnPffrgncntrycd(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    frgncntrycd = models.CharField(db_column='FrgnCntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pffrgncntrycd'


class ReturnPfgrntorcntrapprvfrft(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    grntorcntrapprvfrft_rcpntprsnnm = models.CharField(db_column='GrntOrCntrApprvFrFt_RcpntPrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntbsnssnm_bsnssnmln1txt = models.CharField(db_column='RcpntBsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    rcpntbsnssnm_bsnssnmln2txt = models.CharField(db_column='RcpntBsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_addrssln1txt = models.CharField(db_column='RcpntUSAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_addrssln2txt = models.CharField(db_column='RcpntUSAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_ctynm = models.CharField(db_column='RcpntUSAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_sttabbrvtncd = models.CharField(db_column='RcpntUSAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_zipcd = models.CharField(db_column='RcpntUSAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_addrssln1txt = models.CharField(db_column='RcpntFrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_addrssln2txt = models.CharField(db_column='RcpntFrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_ctynm = models.TextField(db_column='RcpntFrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_cntrycd = models.CharField(db_column='RcpntFrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_frgnpstlcd = models.TextField(db_column='RcpntFrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_prvncorsttnm = models.TextField(db_column='RcpntFrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    grntorcntrapprvfrft_rcpntrltnshptxt = models.CharField(db_column='GrntOrCntrApprvFrFt_RcpntRltnshpTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    grntorcntrapprvfrft_rcpntfndtnsttstxt = models.CharField(db_column='GrntOrCntrApprvFrFt_RcpntFndtnSttsTxt', max_length=20, blank=True, null=True)  # Field name made lowercase.
    grntorcntrapprvfrft_grntorcntrbtnprpstxt = models.TextField(db_column='GrntOrCntrApprvFrFt_GrntOrCntrbtnPrpsTxt', blank=True, null=True)  # Field name made lowercase.
    grntorcntrapprvfrft_amt = models.BigIntegerField(db_column='GrntOrCntrApprvFrFt_Amt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfgrntorcntrapprvfrft'


class ReturnPfgrntorcntrbtnpddryr(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    grntorcntrbtnpddryr_rcpntprsnnm = models.CharField(db_column='GrntOrCntrbtnPdDrYr_RcpntPrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntbsnssnm_bsnssnmln1txt = models.CharField(db_column='RcpntBsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    rcpntbsnssnm_bsnssnmln2txt = models.CharField(db_column='RcpntBsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_addrssln1txt = models.CharField(db_column='RcpntUSAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_addrssln2txt = models.CharField(db_column='RcpntUSAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_ctynm = models.CharField(db_column='RcpntUSAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_sttabbrvtncd = models.CharField(db_column='RcpntUSAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rcpntusaddrss_zipcd = models.CharField(db_column='RcpntUSAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_addrssln1txt = models.CharField(db_column='RcpntFrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_addrssln2txt = models.CharField(db_column='RcpntFrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_ctynm = models.TextField(db_column='RcpntFrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_cntrycd = models.CharField(db_column='RcpntFrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_frgnpstlcd = models.TextField(db_column='RcpntFrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    rcpntfrgnaddrss_prvncorsttnm = models.TextField(db_column='RcpntFrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    grntorcntrbtnpddryr_rcpntrltnshptxt = models.CharField(db_column='GrntOrCntrbtnPdDrYr_RcpntRltnshpTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    grntorcntrbtnpddryr_rcpntfndtnsttstxt = models.CharField(db_column='GrntOrCntrbtnPdDrYr_RcpntFndtnSttsTxt', max_length=20, blank=True, null=True)  # Field name made lowercase.
    grntorcntrbtnpddryr_grntorcntrbtnprpstxt = models.TextField(db_column='GrntOrCntrbtnPdDrYr_GrntOrCntrbtnPrpsTxt', blank=True, null=True)  # Field name made lowercase.
    grntorcntrbtnpddryr_amt = models.BigIntegerField(db_column='GrntOrCntrbtnPdDrYr_Amt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfgrntorcntrbtnpddryr'


class ReturnPfoffcrdrtrstkyempl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    offcrdrtrstkyemplinf_offcrdrtrstkyempl = models.TextField(db_column='OffcrDrTrstKyEmplInf_OffcrDrTrstKyEmpl', blank=True, null=True)  # Field name made lowercase.
    offcrdrtrstkyempl_prsnnm = models.TextField(db_column='OffcrDrTrstKyEmpl_PrsnNm', blank=True, null=True)  # Field name made lowercase.
    offcrdrtrstkyempl_bsnssnmln1 = models.TextField(db_column='OffcrDrTrstKyEmpl_BsnssNmLn1', blank=True, null=True)  # Field name made lowercase.
    offcrdrtrstkyempl_bsnssnmln2 = models.TextField(db_column='OffcrDrTrstKyEmpl_BsnssNmLn2', blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    offcrdrtrstkyempl_ttltxt = models.CharField(db_column='OffcrDrTrstKyEmpl_TtlTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    offcrdrtrstkyempl_avrghrsprwkdvtdtpsrt = models.TextField(db_column='OffcrDrTrstKyEmpl_AvrgHrsPrWkDvtdTPsRt', blank=True, null=True)  # Field name made lowercase.
    offcrdrtrstkyempl_cmpnstnamt = models.BigIntegerField(db_column='OffcrDrTrstKyEmpl_CmpnstnAmt', blank=True, null=True)  # Field name made lowercase.
    offcrdrtrstkyempl_emplybnftprgrmamt = models.BigIntegerField(db_column='OffcrDrTrstKyEmpl_EmplyBnftPrgrmAmt', blank=True, null=True)  # Field name made lowercase.
    offcrdrtrstkyempl_expnsaccntothrallwncamt = models.BigIntegerField(db_column='OffcrDrTrstKyEmpl_ExpnsAccntOthrAllwncAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfoffcrdrtrstkyempl'


class ReturnPforgrprtorrgstrsttcd(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    orgrprtorrgstrsttcd = models.CharField(db_column='OrgRprtOrRgstrSttCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pforgrprtorrgstrsttcd'


class ReturnPfothrrvndscrbd(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dsc = models.CharField(db_column='Dsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bsnsscd = models.TextField(db_column='BsnssCd', blank=True, null=True)  # Field name made lowercase.
    unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    exclsncd = models.TextField(db_column='ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    exclsnamt = models.BigIntegerField(db_column='ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfothrrvndscrbd'


class ReturnPfprgrmsrvcrvprtvii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dsc = models.CharField(db_column='Dsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bsnsscd = models.TextField(db_column='BsnssCd', blank=True, null=True)  # Field name made lowercase.
    unrltdbsnsstxblincmamt = models.BigIntegerField(db_column='UnrltdBsnssTxblIncmAmt', blank=True, null=True)  # Field name made lowercase.
    exclsncd = models.TextField(db_column='ExclsnCd', blank=True, null=True)  # Field name made lowercase.
    exclsnamt = models.BigIntegerField(db_column='ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    rltdorexmptfnctnincmamt = models.BigIntegerField(db_column='RltdOrExmptFnctnIncmAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfprgrmsrvcrvprtvii'


class ReturnPfrlnofactytaccmofexmptprps(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    rlnofactytaccmofexmptprps = models.TextField(db_column='RlnOfActyTAccmOfExmptPrps', blank=True, null=True)  # Field name made lowercase.
    lnnmbrtxt = models.TextField(db_column='LnNmbrTxt', blank=True, null=True)  # Field name made lowercase.
    rltnshpsttmnttxt = models.TextField(db_column='RltnshpSttmntTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfrlnofactytaccmofexmptprps'


class ReturnPfrltnshpskddtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    orgnztndsc = models.CharField(db_column='OrgnztnDsc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rltnshpdscrptntxt = models.TextField(db_column='RltnshpDscrptnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfrltnshpskddtl'


class ReturnPfshrhldrmngrnm(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    shrhldrmngrnm = models.CharField(db_column='ShrhldrMngrNm', max_length=35, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfshrhldrmngrnm'


class ReturnPfspclcndtndsc(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spclcndtndsc = models.TextField(db_column='SpclCndtnDsc', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pfspclcndtndsc'


class ReturnPftrnsfrskddtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    lnnmbrtxt = models.TextField(db_column='LnNmbrTxt', blank=True, null=True)  # Field name made lowercase.
    invlvdamt = models.BigIntegerField(db_column='InvlvdAmt', blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    trnsfrstrnsandshrarrngmdsc = models.TextField(db_column='TrnsfrsTrnsAndShrArrngmDsc', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_pftrnsfrskddtl'


class ReturnPrgrmsrvcrvn(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dsc = models.CharField(db_column='Dsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ttlrvnclmnamt = models.BigIntegerField(db_column='TtlRvnClmnAmt', blank=True, null=True)  # Field name made lowercase.
    rltdorexmptfncincmamt = models.BigIntegerField(db_column='RltdOrExmptFncIncmAmt', blank=True, null=True)  # Field name made lowercase.
    unrltdbsnssrvnamt = models.BigIntegerField(db_column='UnrltdBsnssRvnAmt', blank=True, null=True)  # Field name made lowercase.
    exclsnamt = models.BigIntegerField(db_column='ExclsnAmt', blank=True, null=True)  # Field name made lowercase.
    bsnsscd = models.TextField(db_column='BsnssCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_prgrmsrvcrvn'


class ReturnPrgsrvcaccmactyothr(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    actvtycd = models.BigIntegerField(db_column='ActvtyCd', blank=True, null=True)  # Field name made lowercase.
    expnsamt = models.BigIntegerField(db_column='ExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    grntamt = models.BigIntegerField(db_column='GrntAmt', blank=True, null=True)  # Field name made lowercase.
    rvnamt = models.BigIntegerField(db_column='RvnAmt', blank=True, null=True)  # Field name made lowercase.
    dsc = models.TextField(db_column='Dsc', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_prgsrvcaccmactyothr'


class ReturnReturnheader990XPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    rtrnhdr_rtrnts = models.CharField(db_column='RtrnHdr_RtrnTs', max_length=63, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_txprdenddt = models.CharField(db_column='RtrnHdr_TxPrdEndDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_dsstrrlftxt = models.CharField(db_column='RtrnHdr_DsstrRlfTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_ispnm = models.CharField(db_column='RtrnHdr_ISPNm', max_length=6, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_prprrfrm = models.TextField(db_column='RtrnHdr_PrprrFrm', blank=True, null=True)  # Field name made lowercase.
    prprrfrm_prprrfrmein = models.CharField(db_column='PrprrFrm_PrprrFrmEIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    prprrfrmnm_bsnssnmln1txt = models.CharField(db_column='PrprrFrmNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    prprrfrmnm_bsnssnmln2txt = models.CharField(db_column='PrprrFrmNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    prprrusaddrss_addrssln1txt = models.CharField(db_column='PrprrUSAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    prprrusaddrss_addrssln2txt = models.CharField(db_column='PrprrUSAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    prprrusaddrss_ctynm = models.CharField(db_column='PrprrUSAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    prprrusaddrss_sttabbrvtncd = models.CharField(db_column='PrprrUSAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    prprrusaddrss_zipcd = models.CharField(db_column='PrprrUSAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    prprrfrgnaddrss_addrssln1txt = models.CharField(db_column='PrprrFrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    prprrfrgnaddrss_addrssln2txt = models.CharField(db_column='PrprrFrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    prprrfrgnaddrss_ctynm = models.TextField(db_column='PrprrFrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    prprrfrgnaddrss_prvncorsttnm = models.TextField(db_column='PrprrFrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    prprrfrgnaddrss_cntrycd = models.CharField(db_column='PrprrFrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    prprrfrgnaddrss_frgnpstlcd = models.TextField(db_column='PrprrFrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_sftwrid = models.CharField(db_column='RtrnHdr_SftwrId', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_sftwrvrsnnm = models.CharField(db_column='RtrnHdr_SftwrVrsnNm', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_mltsftwrpckgsusdind = models.CharField(db_column='RtrnHdr_MltSftwrPckgsUsdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_orgntr = models.TextField(db_column='RtrnHdr_Orgntr', blank=True, null=True)  # Field name made lowercase.
    orgntr_efin = models.CharField(db_column='Orgntr_EFIN', max_length=6, blank=True, null=True)  # Field name made lowercase.
    orgntr_orgntrcd = models.CharField(db_column='Orgntr_OrgntrCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    orgntr_prcttnrpin = models.TextField(db_column='Orgntr_PrcttnrPIN', blank=True, null=True)  # Field name made lowercase.
    prcttnrpin_efin = models.CharField(db_column='PrcttnrPIN_EFIN', max_length=6, blank=True, null=True)  # Field name made lowercase.
    prcttnrpin_pin = models.CharField(db_column='PrcttnrPIN_PIN', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_pinentrdbycd = models.TextField(db_column='RtrnHdr_PINEntrdByCd', blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_sgntroptncd = models.TextField(db_column='RtrnHdr_SgntrOptnCd', blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_rtrncd = models.TextField(db_column='RtrnHdr_RtrnCd', blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_txprdbgndt = models.CharField(db_column='RtrnHdr_TxPrdBgnDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_flr = models.TextField(db_column='RtrnHdr_Flr', blank=True, null=True)  # Field name made lowercase.
    flr_ein = models.CharField(db_column='Flr_EIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln1txt = models.CharField(db_column='BsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln2txt = models.CharField(db_column='BsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    flr_incrofnm = models.CharField(db_column='Flr_InCrOfNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    flr_bsnssnmcntrltxt = models.CharField(db_column='Flr_BsnssNmCntrlTxt', max_length=7, blank=True, null=True)  # Field name made lowercase.
    flr_phnnm = models.CharField(db_column='Flr_PhnNm', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_bsnssoffcr = models.TextField(db_column='RtrnHdr_BsnssOffcr', blank=True, null=True)  # Field name made lowercase.
    bsnssoffcr_prsnnm = models.CharField(db_column='BsnssOffcr_PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssoffcr_prsnttltxt = models.CharField(db_column='BsnssOffcr_PrsnTtlTxt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssoffcr_phnnm = models.CharField(db_column='BsnssOffcr_PhnNm', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bsnssoffcr_emladdrsstxt = models.CharField(db_column='BsnssOffcr_EmlAddrssTxt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssoffcr_sgntrdt = models.CharField(db_column='BsnssOffcr_SgntrDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    bsnssoffcr_txpyrpin = models.CharField(db_column='BsnssOffcr_TxpyrPIN', max_length=5, blank=True, null=True)  # Field name made lowercase.
    bsnssoffcr_dscsswthpdprprrind = models.CharField(db_column='BsnssOffcr_DscssWthPdPrprrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_prprrprsn = models.TextField(db_column='RtrnHdr_PrprrPrsn', blank=True, null=True)  # Field name made lowercase.
    prprrprsn_prprrprsnnm = models.CharField(db_column='PrprrPrsn_PrprrPrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    prprrprsn_phnnm = models.CharField(db_column='PrprrPrsn_PhnNm', max_length=10, blank=True, null=True)  # Field name made lowercase.
    prprrprsn_emladdrsstxt = models.CharField(db_column='PrprrPrsn_EmlAddrssTxt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    prprrprsn_prprtndt = models.CharField(db_column='PrprrPrsn_PrprtnDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    prprrprsn_slfemplydind = models.CharField(db_column='PrprrPrsn_SlfEmplydInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prprrprsn_ssn = models.CharField(db_column='PrprrPrsn_SSN', max_length=12, blank=True, null=True)  # Field name made lowercase.
    prprrprsn_ptin = models.CharField(db_column='PrprrPrsn_PTIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_flngscrtyinfrmtn = models.TextField(db_column='RtrnHdr_FlngScrtyInfrmtn', blank=True, null=True)  # Field name made lowercase.
    ipaddrss_ipv4addrsstxt = models.CharField(db_column='IPAddrss_IPv4AddrssTxt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    ipaddrss_ipv6addrsstxt = models.CharField(db_column='IPAddrss_IPv6AddrssTxt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    flngscrtyinfrmtn_ipdt = models.CharField(db_column='FlngScrtyInfrmtn_IPDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    flngscrtyinfrmtn_iptm = models.CharField(db_column='FlngScrtyInfrmtn_IPTm', max_length=15, blank=True, null=True)  # Field name made lowercase.
    flngscrtyinfrmtn_iptmzncd = models.CharField(db_column='FlngScrtyInfrmtn_IPTmznCd', max_length=31, blank=True, null=True)  # Field name made lowercase.
    flngscrtyinfrmtn_fdrlorgnlsbmssnid = models.TextField(db_column='FlngScrtyInfrmtn_FdrlOrgnlSbmssnId', blank=True, null=True)  # Field name made lowercase.
    flngscrtyinfrmtn_fdrlorgnlsbmssniddt = models.CharField(db_column='FlngScrtyInfrmtn_FdrlOrgnlSbmssnIdDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    flngscrtyinfrmtn_flnglcnscd = models.TextField(db_column='FlngScrtyInfrmtn_FlngLcnsCd', blank=True, null=True)  # Field name made lowercase.
    flngscrtyinfrmtn_atsbmssncrtndvcid = models.CharField(db_column='FlngScrtyInfrmtn_AtSbmssnCrtnDvcId', max_length=40, blank=True, null=True)  # Field name made lowercase.
    flngscrtyinfrmtn_atsbmssnflngdvcid = models.CharField(db_column='FlngScrtyInfrmtn_AtSbmssnFlngDvcId', max_length=40, blank=True, null=True)  # Field name made lowercase.
    rtrnhdr_txyr = models.IntegerField(db_column='RtrnHdr_TxYr', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_returnheader990x_part_i'


class ReturnSkdaagrcltrlnmandaddrss(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    ctynm = models.CharField(db_column='CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    sttabbrvtncd = models.CharField(db_column='SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cntrycd = models.CharField(db_column='CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdaagrcltrlnmandaddrss'


class ReturnSkdafrm990Skdaprtvi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    frm990skdaprtvi = models.TextField(db_column='Frm990SkdAPrtVI', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdafrm990skdaprtvi'


class ReturnSkdahsptlnmandaddrss(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    ctynm = models.CharField(db_column='CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    sttabbrvtncd = models.CharField(db_column='SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cntrycd = models.CharField(db_column='CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdahsptlnmandaddrss'


class ReturnSkdaspprtdorginfrmtn(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    orgnztncd = models.TextField(db_column='OrgnztnCd', blank=True, null=True)  # Field name made lowercase.
    othrspprtamt = models.BigIntegerField(db_column='OthrSpprtAmt', blank=True, null=True)  # Field name made lowercase.
    spprtdorgein = models.CharField(db_column='SpprtdOrgEIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    gvrnngdcmntlstdind = models.CharField(db_column='GvrnngDcmntLstdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    spprtamt = models.BigIntegerField(db_column='SpprtAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdaspprtdorginfrmtn'


class ReturnSkdbchrtblcntrbtnsdtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    chrtblcntrbtnsdtl_cntrbtrnm = models.BigIntegerField(db_column='ChrtblCntrbtnsDtl_CntrbtrNm', blank=True, null=True)  # Field name made lowercase.
    chrtblcntrbtnsdtl_gftprpstxt = models.CharField(db_column='ChrtblCntrbtnsDtl_GftPrpsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    chrtblcntrbtnsdtl_gftustxt = models.CharField(db_column='ChrtblCntrbtnsDtl_GftUsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    chrtblcntrbtnsdtl_hwgftishlddsc = models.CharField(db_column='ChrtblCntrbtnsDtl_HwGftIsHldDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    chrtblcntrbtnsdtl_rlnoftrnsfrrttrnsfrtxt = models.CharField(db_column='ChrtblCntrbtnsDtl_RlnOfTrnsfrrTTrnsfrTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    trnsfrnmbsnss_bsnssnmln1txt = models.CharField(db_column='TrnsfrNmBsnss_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    trnsfrnmbsnss_bsnssnmln2txt = models.CharField(db_column='TrnsfrNmBsnss_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    chrtblcntrbtnsdtl_trnsfrnmindvdl = models.CharField(db_column='ChrtblCntrbtnsDtl_TrnsfrNmIndvdl', max_length=35, blank=True, null=True)  # Field name made lowercase.
    trnsfrusaddrss_addrssln1txt = models.CharField(db_column='TrnsfrUSAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    trnsfrusaddrss_addrssln2txt = models.CharField(db_column='TrnsfrUSAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    trnsfrusaddrss_ctynm = models.CharField(db_column='TrnsfrUSAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    trnsfrusaddrss_sttabbrvtncd = models.CharField(db_column='TrnsfrUSAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    trnsfrusaddrss_zipcd = models.CharField(db_column='TrnsfrUSAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    trnsfrfrgnaddrss_addrssln1txt = models.CharField(db_column='TrnsfrFrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    trnsfrfrgnaddrss_addrssln2txt = models.CharField(db_column='TrnsfrFrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    trnsfrfrgnaddrss_ctynm = models.TextField(db_column='TrnsfrFrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    trnsfrfrgnaddrss_prvncorsttnm = models.TextField(db_column='TrnsfrFrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    trnsfrfrgnaddrss_cntrycd = models.CharField(db_column='TrnsfrFrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    trnsfrfrgnaddrss_frgnpstlcd = models.TextField(db_column='TrnsfrFrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdbchrtblcntrbtnsdtl'


class ReturnSkdbcntrbtrinfrmtn(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    cntrbtrinfrmtn_cntrbtrnm = models.BigIntegerField(db_column='CntrbtrInfrmtn_CntrbtrNm', blank=True, null=True)  # Field name made lowercase.
    cntrbtrinfrmtn_ttlcntrbtnsamt = models.BigIntegerField(db_column='CntrbtrInfrmtn_TtlCntrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    cntrbtrinfrmtn_prsncntrbtnind = models.CharField(db_column='CntrbtrInfrmtn_PrsnCntrbtnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cntrbtrinfrmtn_pyrllcntrbtnind = models.CharField(db_column='CntrbtrInfrmtn_PyrllCntrbtnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cntrbtrinfrmtn_nncshcntrbtnind = models.CharField(db_column='CntrbtrInfrmtn_NncshCntrbtnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cntrbtrbsnssnm_bsnssnmln1txt = models.CharField(db_column='CntrbtrBsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    cntrbtrbsnssnm_bsnssnmln2txt = models.CharField(db_column='CntrbtrBsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    cntrbtrinfrmtn_cntrbtrprsnnm = models.CharField(db_column='CntrbtrInfrmtn_CntrbtrPrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    cntrbtrinfrmtn_pd527j1ind = models.CharField(db_column='CntrbtrInfrmtn_Pd527j1Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cntrbtrusaddrss_addrssln1txt = models.CharField(db_column='CntrbtrUSAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    cntrbtrusaddrss_addrssln2txt = models.CharField(db_column='CntrbtrUSAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    cntrbtrusaddrss_ctynm = models.CharField(db_column='CntrbtrUSAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    cntrbtrusaddrss_sttabbrvtncd = models.CharField(db_column='CntrbtrUSAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cntrbtrusaddrss_zipcd = models.CharField(db_column='CntrbtrUSAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    cntrbtrfrgnaddrss_addrssln1txt = models.CharField(db_column='CntrbtrFrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    cntrbtrfrgnaddrss_addrssln2txt = models.CharField(db_column='CntrbtrFrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    cntrbtrfrgnaddrss_ctynm = models.TextField(db_column='CntrbtrFrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    cntrbtrfrgnaddrss_prvncorsttnm = models.TextField(db_column='CntrbtrFrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    cntrbtrfrgnaddrss_cntrycd = models.CharField(db_column='CntrbtrFrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cntrbtrfrgnaddrss_frgnpstlcd = models.TextField(db_column='CntrbtrFrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdbcntrbtrinfrmtn'


class ReturnSkdbnncshprprtycntrbtn(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    cntrbtrnm = models.BigIntegerField(db_column='CntrbtrNm', blank=True, null=True)  # Field name made lowercase.
    nncshprprtydsc = models.CharField(db_column='NncshPrprtyDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    frmrktvlamt = models.BigIntegerField(db_column='FrMrktVlAmt', blank=True, null=True)  # Field name made lowercase.
    rcvddt = models.CharField(db_column='RcvdDt', max_length=31, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdbnncshprprtycntrbtn'


class ReturnSkdcsctn527Pltclorg(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdc_sctn527pltclorg = models.TextField(db_column='SkdC_Sctn527PltclOrg', blank=True, null=True)  # Field name made lowercase.
    orgnztnbsnssnm_bsnssnmln1txt = models.CharField(db_column='OrgnztnBsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    orgnztnbsnssnm_bsnssnmln2txt = models.CharField(db_column='OrgnztnBsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    sctn527pltclorg_ein = models.CharField(db_column='Sctn527PltclOrg_EIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    sctn527pltclorg_pdintrnlfndsamt = models.BigIntegerField(db_column='Sctn527PltclOrg_PdIntrnlFndsAmt', blank=True, null=True)  # Field name made lowercase.
    sctn527pltclorg_cntrbtnsrcvddlvramt = models.BigIntegerField(db_column='Sctn527PltclOrg_CntrbtnsRcvdDlvrAmt', blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdcsctn527pltclorg'


class ReturnSkdcspplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdcspplmntlinfrmtndtl'


class ReturnSkddinvstprgrmrltdorg(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dsc = models.CharField(db_column='Dsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bkvlamt = models.BigIntegerField(db_column='BkVlAmt', blank=True, null=True)  # Field name made lowercase.
    mthdvltncd = models.TextField(db_column='MthdVltnCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skddinvstprgrmrltdorg'


class ReturnSkddothrasstsorg(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dsc = models.CharField(db_column='Dsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bkvlamt = models.BigIntegerField(db_column='BkVlAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skddothrasstsorg'


class ReturnSkddothrlbltsorg(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dsc = models.CharField(db_column='Dsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    amt = models.BigIntegerField(db_column='Amt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skddothrlbltsorg'


class ReturnSkddothrscrts(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dsc = models.CharField(db_column='Dsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bkvlamt = models.BigIntegerField(db_column='BkVlAmt', blank=True, null=True)  # Field name made lowercase.
    mthdvltncd = models.TextField(db_column='MthdVltnCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skddothrscrts'


class ReturnSkddspplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skddspplmntlinfrmtndtl'


class ReturnSkdespplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdespplmntlinfrmtndtl'


class ReturnSkdfaccntactvtsotsdus(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    rgntxt = models.CharField(db_column='RgnTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    offcscnt = models.BigIntegerField(db_column='OffcsCnt', blank=True, null=True)  # Field name made lowercase.
    emplycnt = models.BigIntegerField(db_column='EmplyCnt', blank=True, null=True)  # Field name made lowercase.
    ofactvtscndctdtxt = models.CharField(db_column='OfActvtsCndctdTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    spcfcsrvcsprvddtxt = models.TextField(db_column='SpcfcSrvcsPrvddTxt', blank=True, null=True)  # Field name made lowercase.
    rgnttlexpndtrsamt = models.BigIntegerField(db_column='RgnTtlExpndtrsAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdfaccntactvtsotsdus'


class ReturnSkdffrgnindvdlsgrnts(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    ofassstnctxt = models.TextField(db_column='OfAssstncTxt', blank=True, null=True)  # Field name made lowercase.
    rgntxt = models.CharField(db_column='RgnTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rcpntcnt = models.BigIntegerField(db_column='RcpntCnt', blank=True, null=True)  # Field name made lowercase.
    cshgrntamt = models.BigIntegerField(db_column='CshGrntAmt', blank=True, null=True)  # Field name made lowercase.
    mnnrofcshdsbrsmnttxt = models.CharField(db_column='MnnrOfCshDsbrsmntTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nncshassstncamt = models.BigIntegerField(db_column='NnCshAssstncAmt', blank=True, null=True)  # Field name made lowercase.
    dscrptnofnncshassttxt = models.TextField(db_column='DscrptnOfNnCshAsstTxt', blank=True, null=True)  # Field name made lowercase.
    vltnmthdusddsc = models.CharField(db_column='VltnMthdUsdDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdffrgnindvdlsgrnts'


class ReturnSkdfgrntstorgotsdus(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    rgntxt = models.CharField(db_column='RgnTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prpsofgrnttxt = models.TextField(db_column='PrpsOfGrntTxt', blank=True, null=True)  # Field name made lowercase.
    cshgrntamt = models.BigIntegerField(db_column='CshGrntAmt', blank=True, null=True)  # Field name made lowercase.
    mnnrofcshdsbrsmnttxt = models.CharField(db_column='MnnrOfCshDsbrsmntTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nncshassstncamt = models.BigIntegerField(db_column='NnCshAssstncAmt', blank=True, null=True)  # Field name made lowercase.
    dscrptnofnncshassttxt = models.TextField(db_column='DscrptnOfNnCshAsstTxt', blank=True, null=True)  # Field name made lowercase.
    vltnmthdusddsc = models.CharField(db_column='VltnMthdUsdDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdfgrntstorgotsdus'


class ReturnSkdfspplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdfspplmntlinfrmtndtl'


class ReturnSkdgfndrsractvtyinf(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    fndrsractvtyinf_prsnnm = models.CharField(db_column='FndrsrActvtyInf_PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    orgnztnbsnssnm_bsnssnmln1txt = models.CharField(db_column='OrgnztnBsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    orgnztnbsnssnm_bsnssnmln2txt = models.CharField(db_column='OrgnztnBsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    fndrsractvtyinf_actvtytxt = models.TextField(db_column='FndrsrActvtyInf_ActvtyTxt', blank=True, null=True)  # Field name made lowercase.
    fndrsractvtyinf_fndrsrcntrloffndsind = models.CharField(db_column='FndrsrActvtyInf_FndrsrCntrlOfFndsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fndrsractvtyinf_grssrcptsamt = models.BigIntegerField(db_column='FndrsrActvtyInf_GrssRcptsAmt', blank=True, null=True)  # Field name made lowercase.
    fndrsractvtyinf_rtndbycntrctramt = models.BigIntegerField(db_column='FndrsrActvtyInf_RtndByCntrctrAmt', blank=True, null=True)  # Field name made lowercase.
    fndrsractvtyinf_nttorgnztnamt = models.BigIntegerField(db_column='FndrsrActvtyInf_NtTOrgnztnAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdgfndrsractvtyinf'


class ReturnSkdglcnsdsttscd(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    lcnsdsttscd = models.CharField(db_column='LcnsdSttsCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdglcnsdsttscd'


class ReturnSkdgspplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdgspplmntlinfrmtndtl'


class ReturnSkdgsttswhrgmngcndctdcd(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    sttswhrgmngcndctdcd = models.CharField(db_column='SttsWhrGmngCndctdCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdgsttswhrgmngcndctdcd'


class ReturnSkdhhsptlfclts(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdh_hsptlfclts = models.TextField(db_column='SkdH_HsptlFclts', blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_fcltynm = models.IntegerField(db_column='HsptlFclts_FcltyNm', blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln1txt = models.CharField(db_column='BsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln2txt = models.CharField(db_column='BsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_wbstaddrsstxt = models.CharField(db_column='HsptlFclts_WbstAddrssTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_sttlcnsnm = models.TextField(db_column='HsptlFclts_SttLcnsNm', blank=True, null=True)  # Field name made lowercase.
    sbrdnthsptlnm_bsnssnmln1txt = models.CharField(db_column='SbrdntHsptlNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    sbrdnthsptlnm_bsnssnmln2txt = models.CharField(db_column='SbrdntHsptlNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_sbrdnthsptlein = models.CharField(db_column='HsptlFclts_SbrdntHsptlEIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_lcnsdhsptlind = models.CharField(db_column='HsptlFclts_LcnsdHsptlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_gnrlmdclandsrgclind = models.CharField(db_column='HsptlFclts_GnrlMdclAndSrgclInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_chldrnshsptlind = models.CharField(db_column='HsptlFclts_ChldrnsHsptlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_tchnghsptlind = models.CharField(db_column='HsptlFclts_TchngHsptlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_crtclaccsshsptlind = models.CharField(db_column='HsptlFclts_CrtclAccssHsptlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_rsrchfcltyind = models.CharField(db_column='HsptlFclts_RsrchFcltyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_emrgncyrm24hrsind = models.CharField(db_column='HsptlFclts_EmrgncyRm24HrsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_emrgncyrmothrind = models.CharField(db_column='HsptlFclts_EmrgncyRmOthrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_othrdsc = models.CharField(db_column='HsptlFclts_OthrDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hsptlfclts_fcltyrprtnggrpcd = models.TextField(db_column='HsptlFclts_FcltyRprtngGrpCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdhhsptlfclts'


class ReturnSkdhhsptlfcltyplcsprctc(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    hsptlfcltyplcsprctc = models.TextField(db_column='HsptlFcltyPlcsPrctc', blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    fcltynm = models.IntegerField(db_column='FcltyNm', blank=True, null=True)  # Field name made lowercase.
    frstlcnsdcyorpyind = models.CharField(db_column='FrstLcnsdCYOrPYInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txexmpthsptlcyorpyind = models.CharField(db_column='TxExmptHsptlCYOrPYInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    chnacndctdind = models.CharField(db_column='CHNACndctdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cmmntydfntnind = models.CharField(db_column='CmmntyDfntnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cmmntydmgrphcsind = models.CharField(db_column='CmmntyDmgrphcsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    exstngrsrcsind = models.CharField(db_column='ExstngRsrcsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hwdtobtndind = models.CharField(db_column='HwDtObtndInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cmmntyhlthndsind = models.CharField(db_column='CmmntyHlthNdsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othrhlthisssind = models.CharField(db_column='OthrHlthIsssInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cmmntyhlthndsidprcssind = models.CharField(db_column='CmmntyHlthNdsIdPrcssInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cnsltngprcssind = models.CharField(db_column='CnsltngPrcssInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prrchnaimpctind = models.CharField(db_column='PrrCHNAImpctInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othrind = models.CharField(db_column='OthrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    chnacndctdyr = models.TextField(db_column='CHNACndctdYr', blank=True, null=True)  # Field name made lowercase.
    tkintaccntothrsinptind = models.CharField(db_column='TkIntAccntOthrsInptInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    chnacndctdwthothrfcltsind = models.CharField(db_column='CHNACndctdWthOthrFcltsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    chnacndctdwthnnfcltsind = models.CharField(db_column='CHNACndctdWthNnFcltsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    chnarprtwdlyavlblind = models.CharField(db_column='CHNARprtWdlyAvlblInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rptavlblonownwbstind = models.CharField(db_column='RptAvlblOnOwnWbstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ownwbsturltxt = models.CharField(db_column='OwnWbstURLTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    othrwbstind = models.CharField(db_column='OthrWbstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othrwbsturltxt = models.CharField(db_column='OthrWbstURLTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pprcpypblcinspctnind = models.CharField(db_column='PprCpyPblcInspctnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rptavlblthrothrmthdind = models.CharField(db_column='RptAvlblThrOthrMthdInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    implmnttnstrtgyadptind = models.CharField(db_column='ImplmnttnStrtgyAdptInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    implmnttnstrtgyadptyr = models.TextField(db_column='ImplmnttnStrtgyAdptYr', blank=True, null=True)  # Field name made lowercase.
    strtgypstdwbstind = models.CharField(db_column='StrtgyPstdWbstInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    strtgywbsturltxt = models.CharField(db_column='StrtgyWbstURLTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    strtgyattchdind = models.TextField(db_column='StrtgyAttchdInd', blank=True, null=True)  # Field name made lowercase.
    orgnztnincrexcstxind = models.CharField(db_column='OrgnztnIncrExcsTxInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm4720fldind = models.CharField(db_column='Frm4720FldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    excsrprtfrm4720frallamt = models.BigIntegerField(db_column='ExcsRprtFrm4720FrAllAmt', blank=True, null=True)  # Field name made lowercase.
    elgcrtrexplndind = models.CharField(db_column='ElgCrtrExplndInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fpgfmlyincmlmtfrdscntind = models.CharField(db_column='FPGFmlyIncmLmtFrDscntInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fpgfmlyincmlmtfrcrpct = models.DecimalField(db_column='FPGFmlyIncmLmtFrCrPct', max_digits=22, decimal_places=12, blank=True, null=True)  # Field name made lowercase.
    fpgfmlyincmlmtdscntcrpct = models.DecimalField(db_column='FPGFmlyIncmLmtDscntCrPct', max_digits=22, decimal_places=12, blank=True, null=True)  # Field name made lowercase.
    incmlvlcrtrind = models.CharField(db_column='IncmLvlCrtrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    asstlvlcrtrind = models.CharField(db_column='AsstLvlCrtrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mdclindgncycrtrind = models.CharField(db_column='MdclIndgncyCrtrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    insrncsttscrtrind = models.CharField(db_column='InsrncSttsCrtrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    undrnsrncsttcrtrind = models.CharField(db_column='UndrnsrncSttCrtrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rsdncycrtrind = models.CharField(db_column='RsdncyCrtrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othrcrtrind = models.CharField(db_column='OthrCrtrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    explndbssind = models.CharField(db_column='ExplndBssInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    appfnnclasstexplnind = models.CharField(db_column='AppFnnclAsstExplnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dscrbdinfind = models.CharField(db_column='DscrbdInfInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dscrbdsprtdcind = models.CharField(db_column='DscrbdSprtDcInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prvddhsptlcntctind = models.CharField(db_column='PrvddHsptlCntctInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prvddnnprftcntctind = models.CharField(db_column='PrvddNnprftCntctInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othrmthdind = models.CharField(db_column='OthrMthdInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    incldspblctymsrsind = models.CharField(db_column='IncldsPblctyMsrsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fapavlblonwbstind = models.CharField(db_column='FAPAvlblOnWbstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fapavlblonwbsturltxt = models.CharField(db_column='FAPAvlblOnWbstURLTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fapappavlblonwbstind = models.CharField(db_column='FAPAppAvlblOnWbstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fapappavlblonwbsturltxt = models.CharField(db_column='FAPAppAvlblOnWbstURLTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fapsmmryonwbstind = models.CharField(db_column='FAPSmmryOnWbstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fapsmmryonwbsturltxt = models.CharField(db_column='FAPSmmryOnWbstURLTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fapavlblonrqstnchrgind = models.CharField(db_column='FAPAvlblOnRqstNChrgInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fapappavlblonrqstnchrgind = models.CharField(db_column='FAPAppAvlblOnRqstNChrgInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fapsmavlblonrqstnchrgind = models.CharField(db_column='FAPSmAvlblOnRqstNChrgInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ntfdfapcpyblldsplyind = models.CharField(db_column='NtfdFAPCpyBllDsplyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cmmnttyntfdfapind = models.CharField(db_column='CmmnttyNtfdFAPInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    faptrnsltdind = models.CharField(db_column='FAPTrnsltdInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othrpblctyind = models.CharField(db_column='OthrPblctyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fapactnsonnnpymntind = models.CharField(db_column='FAPActnsOnNnpymntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prmtrprttcrdtagncyind = models.CharField(db_column='PrmtRprtTCrdtAgncyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prmtsllngdbtind = models.CharField(db_column='PrmtSllngDbtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prmtdfrdnyrqrpymntind = models.CharField(db_column='PrmtDfrDnyRqrPymntInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prmtlgljdclprcssind = models.CharField(db_column='PrmtLglJdclPrcssInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prmtothractnsind = models.CharField(db_column='PrmtOthrActnsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prmtnactnsind = models.CharField(db_column='PrmtNActnsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cllctnactvtsind = models.CharField(db_column='CllctnActvtsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rprtngtcrdtagncyind = models.CharField(db_column='RprtngTCrdtAgncyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enggdsllngdbtind = models.CharField(db_column='EnggdSllngDbtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enggdfrdnyrqrpymntind = models.CharField(db_column='EnggDfrDnyRqrPymntInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enggdlgljdclprcssind = models.CharField(db_column='EnggdLglJdclPrcssInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othractnsind = models.CharField(db_column='OthrActnsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prvddwrttnntcind = models.CharField(db_column='PrvddWrttnNtcInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mdeffrtorllyntfyind = models.CharField(db_column='MdEffrtOrllyNtfyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prcssdfapapplctnind = models.CharField(db_column='PrcssdFAPApplctnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mdprsmptvelgdtrmind = models.CharField(db_column='MdPrsmptvElgDtrmInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othractnstknind = models.CharField(db_column='OthrActnsTknInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nnmdind = models.CharField(db_column='NnMdInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nndsemrgncycrplcyind = models.CharField(db_column='NndsEmrgncyCrPlcyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    nemrgncycrind = models.CharField(db_column='NEmrgncyCrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nemrgncycrplcyind = models.CharField(db_column='NEmrgncyCrPlcyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emrgncycrlmtdind = models.CharField(db_column='EmrgncyCrLmtdInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othrrsnind = models.CharField(db_column='OthrRsnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lkbckmdcrind = models.CharField(db_column='LkBckMdcrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lkbckmdcrprvtind = models.CharField(db_column='LkBckMdcrPrvtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lkbckmdcdmdcrprvtind = models.CharField(db_column='LkBckMdcdMdcrPrvtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prspctvmdcrmdcdind = models.CharField(db_column='PrspctvMdcrMdcdInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    amntsgnrllyblldind = models.CharField(db_column='AmntsGnrllyBlldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    grsschrgsind = models.CharField(db_column='GrssChrgsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdhhsptlfcltyplcsprctc'


class ReturnSkdhmngmntcandjntvntrs(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    mngmntcandjntvntrs = models.TextField(db_column='MngmntCAndJntVntrs', blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    prmryactvtstxt = models.CharField(db_column='PrmryActvtsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    orgprftorownrshppct = models.DecimalField(db_column='OrgPrftOrOwnrshpPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    ofcretcprftorownrshppct = models.DecimalField(db_column='OfcrEtcPrftOrOwnrshpPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    physcnsprftorownrshppct = models.DecimalField(db_column='PhyscnsPrftOrOwnrshpPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdhmngmntcandjntvntrs'


class ReturnSkdhothhlthcrfclts(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    othhlthcrfclts = models.TextField(db_column='OthHlthCrFclts', blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    addrssln1txt = models.CharField(db_column='AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    addrssln2txt = models.CharField(db_column='AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    ctynm = models.CharField(db_column='CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    sttabbrvtncd = models.CharField(db_column='SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    zipcd = models.CharField(db_column='ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    fcltytxt = models.CharField(db_column='FcltyTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdhothhlthcrfclts'


class ReturnSkdhspplmntlinfrmtn(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtn = models.TextField(db_column='SpplmntlInfrmtn', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdhspplmntlinfrmtn'


class ReturnSkdhspplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdhspplmntlinfrmtndtl'


class ReturnSkdigrntsothrassttindvinus(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    grntsothrassttindvinus = models.TextField(db_column='GrntsOthrAsstTIndvInUS', blank=True, null=True)  # Field name made lowercase.
    grnttxt = models.TextField(db_column='GrntTxt', blank=True, null=True)  # Field name made lowercase.
    rcpntcnt = models.BigIntegerField(db_column='RcpntCnt', blank=True, null=True)  # Field name made lowercase.
    cshgrntamt = models.BigIntegerField(db_column='CshGrntAmt', blank=True, null=True)  # Field name made lowercase.
    nncshassstncamt = models.BigIntegerField(db_column='NnCshAssstncAmt', blank=True, null=True)  # Field name made lowercase.
    vltnmthdusddsc = models.CharField(db_column='VltnMthdUsdDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nncshassstncdsc = models.TextField(db_column='NnCshAssstncDsc', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdigrntsothrassttindvinus'


class ReturnSkdircpnttbl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdi_rcpnttbl = models.TextField(db_column='SkdI_RcpntTbl', blank=True, null=True)  # Field name made lowercase.
    rcpntbsnssnm_bsnssnmln1txt = models.CharField(db_column='RcpntBsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    rcpntbsnssnm_bsnssnmln2txt = models.CharField(db_column='RcpntBsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    rcpnttbl_rcpntein = models.CharField(db_column='RcpntTbl_RcpntEIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    rcpnttbl_ircsctndsc = models.CharField(db_column='RcpntTbl_IRCSctnDsc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rcpnttbl_cshgrntamt = models.BigIntegerField(db_column='RcpntTbl_CshGrntAmt', blank=True, null=True)  # Field name made lowercase.
    rcpnttbl_nncshassstncamt = models.BigIntegerField(db_column='RcpntTbl_NnCshAssstncAmt', blank=True, null=True)  # Field name made lowercase.
    rcpnttbl_vltnmthdusddsc = models.CharField(db_column='RcpntTbl_VltnMthdUsdDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rcpnttbl_nncshassstncdsc = models.CharField(db_column='RcpntTbl_NnCshAssstncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rcpnttbl_prpsofgrnttxt = models.TextField(db_column='RcpntTbl_PrpsOfGrntTxt', blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdircpnttbl'


class ReturnSkdispplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdispplmntlinfrmtndtl'


class ReturnSkdjrltdorgoffcrtrstkyempl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    rltdorgoffcrtrstkyempl = models.TextField(db_column='RltdOrgOffcrTrstKyEmpl', blank=True, null=True)  # Field name made lowercase.
    prsnnm = models.CharField(db_column='PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    ttltxt = models.CharField(db_column='TtlTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bscmpnstnflngorgamt = models.BigIntegerField(db_column='BsCmpnstnFlngOrgAmt', blank=True, null=True)  # Field name made lowercase.
    cmpnstnbsdonrltdorgsamt = models.BigIntegerField(db_column='CmpnstnBsdOnRltdOrgsAmt', blank=True, null=True)  # Field name made lowercase.
    bnsflngorgnztnamnt = models.BigIntegerField(db_column='BnsFlngOrgnztnAmnt', blank=True, null=True)  # Field name made lowercase.
    bnsrltdorgnztnsamt = models.BigIntegerField(db_column='BnsRltdOrgnztnsAmt', blank=True, null=True)  # Field name made lowercase.
    othrcmpnstnflngorgamt = models.BigIntegerField(db_column='OthrCmpnstnFlngOrgAmt', blank=True, null=True)  # Field name made lowercase.
    othrcmpnstnrltdorgsamt = models.BigIntegerField(db_column='OthrCmpnstnRltdOrgsAmt', blank=True, null=True)  # Field name made lowercase.
    dfrrdcmpnstnflngorgamt = models.BigIntegerField(db_column='DfrrdCmpnstnFlngOrgAmt', blank=True, null=True)  # Field name made lowercase.
    dfrrdcmprltdorgsamt = models.BigIntegerField(db_column='DfrrdCmpRltdOrgsAmt', blank=True, null=True)  # Field name made lowercase.
    nntxblbnftsflngorgamt = models.BigIntegerField(db_column='NntxblBnftsFlngOrgAmt', blank=True, null=True)  # Field name made lowercase.
    nntxblbnftsrltdorgsamt = models.BigIntegerField(db_column='NntxblBnftsRltdOrgsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlcmpnstnflngorgamt = models.BigIntegerField(db_column='TtlCmpnstnFlngOrgAmt', blank=True, null=True)  # Field name made lowercase.
    ttlcmpnstnrltdorgsamt = models.BigIntegerField(db_column='TtlCmpnstnRltdOrgsAmt', blank=True, null=True)  # Field name made lowercase.
    cmprprtprr990flngorgamt = models.BigIntegerField(db_column='CmpRprtPrr990FlngOrgAmt', blank=True, null=True)  # Field name made lowercase.
    cmprprtprr990rltdorgsamt = models.BigIntegerField(db_column='CmpRprtPrr990RltdOrgsAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdjrltdorgoffcrtrstkyempl'


class ReturnSkdjspplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdjspplmntlinfrmtndtl'


class ReturnSkdkprcdrscrrctvactn(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    documentid = models.TextField(db_column='documentId', blank=True, null=True)  # Field name made lowercase.
    bndrfrnccd = models.TextField(db_column='BndRfrncCd', blank=True, null=True)  # Field name made lowercase.
    prcdrscrrctvactnind = models.CharField(db_column='PrcdrsCrrctvActnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdkprcdrscrrctvactn'


class ReturnSkdkspplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    documentid = models.TextField(db_column='documentId', blank=True, null=True)  # Field name made lowercase.
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdkspplmntlinfrmtndtl'


class ReturnSkdktxexmptbndsarbtrg(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    documentid = models.TextField(db_column='documentId', blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_bndrfrnccd = models.TextField(db_column='TxExmptBndsArbtrg_BndRfrncCd', blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_frm8038tfldind = models.CharField(db_column='TxExmptBndsArbtrg_Frm8038TFldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_rbtntdytind = models.CharField(db_column='TxExmptBndsArbtrg_RbtNtDYtInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_excptntrbtind = models.CharField(db_column='TxExmptBndsArbtrg_ExcptnTRbtInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_nrbtdind = models.CharField(db_column='TxExmptBndsArbtrg_NRbtDInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_vrblrtissind = models.CharField(db_column='TxExmptBndsArbtrg_VrblRtIssInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_hdgidntfdinbksandrcind = models.CharField(db_column='TxExmptBndsArbtrg_HdgIdntfdInBksAndRcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    hdgprvdrnm_bsnssnmln1txt = models.CharField(db_column='HdgPrvdrNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    hdgprvdrnm_bsnssnmln2txt = models.CharField(db_column='HdgPrvdrNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_trmofhdgpct = models.DecimalField(db_column='TxExmptBndsArbtrg_TrmOfHdgPct', max_digits=22, decimal_places=12, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_sprntgrtdhdgind = models.CharField(db_column='TxExmptBndsArbtrg_SprntgrtdHdgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_hdgtrmntdind = models.CharField(db_column='TxExmptBndsArbtrg_HdgTrmntdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_grssprcdsinvstdingicind = models.CharField(db_column='TxExmptBndsArbtrg_GrssPrcdsInvstdInGICInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    gicprvdrnm_bsnssnmln1txt = models.CharField(db_column='GICPrvdrNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    gicprvdrnm_bsnssnmln2txt = models.CharField(db_column='GICPrvdrNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_trmofgicpct = models.DecimalField(db_column='TxExmptBndsArbtrg_TrmOfGICPct', max_digits=22, decimal_places=12, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_rgltrysfhrbrstsfdind = models.CharField(db_column='TxExmptBndsArbtrg_RgltrySfHrbrStsfdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_grssprcdsinvstdind = models.CharField(db_column='TxExmptBndsArbtrg_GrssPrcdsInvstdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    txexmptbndsarbtrg_wrttnprctmntrrqsind = models.CharField(db_column='TxExmptBndsArbtrg_WrttnPrcTMntrRqsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdktxexmptbndsarbtrg'


class ReturnSkdktxexmptbndsisss(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    documentid = models.TextField(db_column='documentId', blank=True, null=True)  # Field name made lowercase.
    bndrfrnccd = models.TextField(db_column='BndRfrncCd', blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bndissrein = models.CharField(db_column='BndIssrEIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    cusipnm = models.CharField(db_column='CUSIPNm', max_length=9, blank=True, null=True)  # Field name made lowercase.
    bndissddt = models.CharField(db_column='BndIssdDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    issprcamt = models.BigIntegerField(db_column='IssPrcAmt', blank=True, null=True)  # Field name made lowercase.
    prpsdsc = models.CharField(db_column='PrpsDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dfsdind = models.CharField(db_column='DfsdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    onbhlfofissrind = models.CharField(db_column='OnBhlfOfIssrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    plfnncngind = models.CharField(db_column='PlFnncngInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdktxexmptbndsisss'


class ReturnSkdktxexmptbndsprcds(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    documentid = models.TextField(db_column='documentId', blank=True, null=True)  # Field name made lowercase.
    bndrfrnccd = models.TextField(db_column='BndRfrncCd', blank=True, null=True)  # Field name made lowercase.
    rtrdamt = models.BigIntegerField(db_column='RtrdAmt', blank=True, null=True)  # Field name made lowercase.
    bnddfsdamt = models.BigIntegerField(db_column='BndDfsdAmt', blank=True, null=True)  # Field name made lowercase.
    ttlprcdsamt = models.BigIntegerField(db_column='TtlPrcdsAmt', blank=True, null=True)  # Field name made lowercase.
    inrsrvfndamt = models.BigIntegerField(db_column='InRsrvFndAmt', blank=True, null=True)  # Field name made lowercase.
    cptlzdintrstamt = models.BigIntegerField(db_column='CptlzdIntrstAmt', blank=True, null=True)  # Field name made lowercase.
    rfndngescrwamt = models.BigIntegerField(db_column='RfndngEscrwAmt', blank=True, null=True)  # Field name made lowercase.
    issnccstsfrmprcdsamt = models.BigIntegerField(db_column='IssncCstsFrmPrcdsAmt', blank=True, null=True)  # Field name made lowercase.
    crdtenhncmntamt = models.BigIntegerField(db_column='CrdtEnhncmntAmt', blank=True, null=True)  # Field name made lowercase.
    wrkngcptlexpndtrsamt = models.BigIntegerField(db_column='WrkngCptlExpndtrsAmt', blank=True, null=True)  # Field name made lowercase.
    cptlexpndtrsamt = models.BigIntegerField(db_column='CptlExpndtrsAmt', blank=True, null=True)  # Field name made lowercase.
    othrspntprcdsamt = models.BigIntegerField(db_column='OthrSpntPrcdsAmt', blank=True, null=True)  # Field name made lowercase.
    unspntamt = models.BigIntegerField(db_column='UnspntAmt', blank=True, null=True)  # Field name made lowercase.
    sbstntlcmpltnyr = models.IntegerField(db_column='SbstntlCmpltnYr', blank=True, null=True)  # Field name made lowercase.
    crrntrfndngind = models.CharField(db_column='CrrntRfndngInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    advncrfndngind = models.CharField(db_column='AdvncRfndngInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fnlallctnmdind = models.CharField(db_column='FnlAllctnMdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    adqtbksandrcmntind = models.CharField(db_column='AdqtBksAndRcMntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdktxexmptbndsprcds'


class ReturnSkdktxexmptbndsprvtbsus(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    documentid = models.TextField(db_column='documentId', blank=True, null=True)  # Field name made lowercase.
    bndrfrnccd = models.TextField(db_column='BndRfrncCd', blank=True, null=True)  # Field name made lowercase.
    ownngbndfnncdprprtyind = models.CharField(db_column='OwnngBndFnncdPrprtyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    anylsarrngmntsind = models.CharField(db_column='AnyLsArrngmntsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mgmtcntrctbndfncdprpind = models.CharField(db_column='MgmtCntrctBndFncdPrpInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    enggbndcnslcntrctsind = models.CharField(db_column='EnggBndCnslCntrctsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    anyrsrchagrmntsind = models.CharField(db_column='AnyRsrchAgrmntsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    enggbndcnslrsrchind = models.CharField(db_column='EnggBndCnslRsrchInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prvtbsusbyothrspct = models.DecimalField(db_column='PrvtBsUsByOthrsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    prvtbscncrnngubipct = models.DecimalField(db_column='PrvtBsCncrnngUBIPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    ttlprvtbsnssuspct = models.DecimalField(db_column='TtlPrvtBsnssUsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    bndissmtprvtscpymttstind = models.CharField(db_column='BndIssMtPrvtScPymtTstInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    chnginusbndfnncdprpind = models.CharField(db_column='ChngInUsBndFnncdPrpInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    chnginusbndfnncdprppct = models.DecimalField(db_column='ChngInUsBndFnncdPrpPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    rmdlactntknind = models.CharField(db_column='RmdlActnTknInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prcsnnqlfdbndrmdtdind = models.CharField(db_column='PrcsNnqlfdBndRmdtdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdktxexmptbndsprvtbsus'


class ReturnSkdlbstrinvlvintrstdprsn(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    bstrinvlvintrstdprsn = models.TextField(db_column='BsTrInvlvIntrstdPrsn', blank=True, null=True)  # Field name made lowercase.
    nmofintrstd = models.TextField(db_column='NmOfIntrstd', blank=True, null=True)  # Field name made lowercase.
    prsnnm = models.CharField(db_column='PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    rltnshpdscrptntxt = models.CharField(db_column='RltnshpDscrptnTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    trnsctnamt = models.BigIntegerField(db_column='TrnsctnAmt', blank=True, null=True)  # Field name made lowercase.
    trnsctndsc = models.TextField(db_column='TrnsctnDsc', blank=True, null=True)  # Field name made lowercase.
    shrngofrvnsind = models.CharField(db_column='ShrngOfRvnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdlbstrinvlvintrstdprsn'


class ReturnSkdldsqlfdprsnexbnfttr(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    prsnnm = models.CharField(db_column='PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    rlndsqlfdprsnorgtxt = models.CharField(db_column='RlnDsqlfdPrsnOrgTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    trnsctndsc = models.TextField(db_column='TrnsctnDsc', blank=True, null=True)  # Field name made lowercase.
    trnsctncrrctdind = models.CharField(db_column='TrnsctnCrrctdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdldsqlfdprsnexbnfttr'


class ReturnSkdlgrntasstbnftintrstdprsn(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    grntasstbnftintrstdprsn = models.TextField(db_column='GrntAsstBnftIntrstdPrsn', blank=True, null=True)  # Field name made lowercase.
    prsnnm = models.CharField(db_column='PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    rltnshpwthorgtxt = models.CharField(db_column='RltnshpWthOrgTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cshgrntamt = models.BigIntegerField(db_column='CshGrntAmt', blank=True, null=True)  # Field name made lowercase.
    ofassstnctxt = models.CharField(db_column='OfAssstncTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    assstncprpstxt = models.CharField(db_column='AssstncPrpsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdlgrntasstbnftintrstdprsn'


class ReturnSkdllnsbtwnorgintrstdprsn(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    prsnnm = models.CharField(db_column='PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    lntorgnztnind = models.CharField(db_column='LnTOrgnztnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lnfrmorgnztnind = models.CharField(db_column='LnFrmOrgnztnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rltnshpwthorgtxt = models.CharField(db_column='RltnshpWthOrgTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lnprpstxt = models.CharField(db_column='LnPrpsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    orgnlprncplamt = models.BigIntegerField(db_column='OrgnlPrncplAmt', blank=True, null=True)  # Field name made lowercase.
    blncdamt = models.BigIntegerField(db_column='BlncDAmt', blank=True, null=True)  # Field name made lowercase.
    dfltind = models.CharField(db_column='DfltInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    brdorcmmttapprvlind = models.CharField(db_column='BrdOrCmmttApprvlInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wrttnagrmntind = models.CharField(db_column='WrttnAgrmntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdllnsbtwnorgintrstdprsn'


class ReturnSkdlspplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdlspplmntlinfrmtndtl'


class ReturnSkdmothrnncshcntrtbl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dsc = models.CharField(db_column='Dsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nncshchckbxind = models.CharField(db_column='NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cntrbtncnt = models.BigIntegerField(db_column='CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    mthdofdtrmnngrvnstxt = models.CharField(db_column='MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdmothrnncshcntrtbl'


class ReturnSkdmspplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdmspplmntlinfrmtndtl'


class ReturnSkdndspstnofasstsdtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dspstnofasstsdtl_asstsdstrorexpnsspddsc = models.TextField(db_column='DspstnOfAsstsDtl_AsstsDstrOrExpnssPdDsc', blank=True, null=True)  # Field name made lowercase.
    dspstnofasstsdtl_dstrbtndt = models.CharField(db_column='DspstnOfAsstsDtl_DstrbtnDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    dspstnofasstsdtl_frmrktvlofasstamt = models.BigIntegerField(db_column='DspstnOfAsstsDtl_FrMrktVlOfAsstAmt', blank=True, null=True)  # Field name made lowercase.
    dspstnofasstsdtl_mthdoffmvdtrmntntxt = models.TextField(db_column='DspstnOfAsstsDtl_MthdOfFMVDtrmntnTxt', blank=True, null=True)  # Field name made lowercase.
    dspstnofasstsdtl_ein = models.CharField(db_column='DspstnOfAsstsDtl_EIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    dspstnofasstsdtl_ircsctntxt = models.CharField(db_column='DspstnOfAsstsDtl_IRCSctnTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dspstnofasstsdtl_prsnnm = models.CharField(db_column='DspstnOfAsstsDtl_PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln1txt = models.CharField(db_column='BsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln2txt = models.CharField(db_column='BsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdndspstnofasstsdtl'


class ReturnSkdnlqdtnofasstsdtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    lqdtnofasstsdtl_asstsdstrorexpnsspddsc = models.TextField(db_column='LqdtnOfAsstsDtl_AsstsDstrOrExpnssPdDsc', blank=True, null=True)  # Field name made lowercase.
    lqdtnofasstsdtl_dstrbtndt = models.CharField(db_column='LqdtnOfAsstsDtl_DstrbtnDt', max_length=31, blank=True, null=True)  # Field name made lowercase.
    lqdtnofasstsdtl_frmrktvlofasstamt = models.BigIntegerField(db_column='LqdtnOfAsstsDtl_FrMrktVlOfAsstAmt', blank=True, null=True)  # Field name made lowercase.
    lqdtnofasstsdtl_mthdoffmvdtrmntntxt = models.TextField(db_column='LqdtnOfAsstsDtl_MthdOfFMVDtrmntnTxt', blank=True, null=True)  # Field name made lowercase.
    lqdtnofasstsdtl_ein = models.CharField(db_column='LqdtnOfAsstsDtl_EIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    lqdtnofasstsdtl_ircsctntxt = models.CharField(db_column='LqdtnOfAsstsDtl_IRCSctnTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lqdtnofasstsdtl_prsnnm = models.CharField(db_column='LqdtnOfAsstsDtl_PrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln1txt = models.CharField(db_column='BsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln2txt = models.CharField(db_column='BsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdnlqdtnofasstsdtl'


class ReturnSkdnspplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdnspplmntlinfrmtndtl'


class ReturnSkdospplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdospplmntlinfrmtndtl'


class ReturnSkdriddsrgrddentts(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdr_iddsrgrddentts = models.TextField(db_column='SkdR_IdDsrgrddEntts', blank=True, null=True)  # Field name made lowercase.
    dsrgrddenttynm_bsnssnmln1txt = models.CharField(db_column='DsrgrddEnttyNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    dsrgrddenttynm_bsnssnmln2txt = models.CharField(db_column='DsrgrddEnttyNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    iddsrgrddentts_ein = models.CharField(db_column='IdDsrgrddEntts_EIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    iddsrgrddentts_prmryactvtstxt = models.CharField(db_column='IdDsrgrddEntts_PrmryActvtsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    iddsrgrddentts_ttlincmamt = models.BigIntegerField(db_column='IdDsrgrddEntts_TtlIncmAmt', blank=True, null=True)  # Field name made lowercase.
    iddsrgrddentts_endofyrasstsamt = models.BigIntegerField(db_column='IdDsrgrddEntts_EndOfYrAsstsAmt', blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    iddsrgrddentts_lgldmclsttcd = models.CharField(db_column='IdDsrgrddEntts_LglDmclSttCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    iddsrgrddentts_lgldmclfrgncntrycd = models.CharField(db_column='IdDsrgrddEntts_LglDmclFrgnCntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    drctcntrllngenttynm_bsnssnmln1txt = models.CharField(db_column='DrctCntrllngEnttyNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    drctcntrllngenttynm_bsnssnmln2txt = models.CharField(db_column='DrctCntrllngEnttyNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    iddsrgrddentts_drctcntrllngnacd = models.TextField(db_column='IdDsrgrddEntts_DrctCntrllngNACd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdriddsrgrddentts'


class ReturnSkdridrltdorgtxblcrptr(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdr_idrltdorgtxblcrptr = models.TextField(db_column='SkdR_IdRltdOrgTxblCrpTr', blank=True, null=True)  # Field name made lowercase.
    rltdorgnztnnm_bsnssnmln1txt = models.CharField(db_column='RltdOrgnztnNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    rltdorgnztnnm_bsnssnmln2txt = models.CharField(db_column='RltdOrgnztnNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblcrptr_ein = models.CharField(db_column='IdRltdOrgTxblCrpTr_EIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblcrptr_prmryactvtstxt = models.CharField(db_column='IdRltdOrgTxblCrpTr_PrmryActvtsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblcrptr_enttytxt = models.CharField(db_column='IdRltdOrgTxblCrpTr_EnttyTxt', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblcrptr_shrofttlincmamt = models.BigIntegerField(db_column='IdRltdOrgTxblCrpTr_ShrOfTtlIncmAmt', blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblcrptr_shrofeoyasstsamt = models.BigIntegerField(db_column='IdRltdOrgTxblCrpTr_ShrOfEOYAsstsAmt', blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblcrptr_ownrshppct = models.DecimalField(db_column='IdRltdOrgTxblCrpTr_OwnrshpPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblcrptr_cntrlldorgnztnind = models.CharField(db_column='IdRltdOrgTxblCrpTr_CntrlldOrgnztnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblcrptr_lgldmclsttcd = models.CharField(db_column='IdRltdOrgTxblCrpTr_LglDmclSttCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblcrptr_lgldmclfrgncntrycd = models.CharField(db_column='IdRltdOrgTxblCrpTr_LglDmclFrgnCntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    drctcntrllngenttynm_bsnssnmln1txt = models.CharField(db_column='DrctCntrllngEnttyNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    drctcntrllngenttynm_bsnssnmln2txt = models.CharField(db_column='DrctCntrllngEnttyNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblcrptr_drctcntrllngnacd = models.TextField(db_column='IdRltdOrgTxblCrpTr_DrctCntrllngNACd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdridrltdorgtxblcrptr'


class ReturnSkdridrltdorgtxblprtnrshp(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdr_idrltdorgtxblprtnrshp = models.TextField(db_column='SkdR_IdRltdOrgTxblPrtnrshp', blank=True, null=True)  # Field name made lowercase.
    rltdorgnztnnm_bsnssnmln1txt = models.CharField(db_column='RltdOrgnztnNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    rltdorgnztnnm_bsnssnmln2txt = models.CharField(db_column='RltdOrgnztnNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_ein = models.CharField(db_column='IdRltdOrgTxblPrtnrshp_EIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_prmryactvtstxt = models.CharField(db_column='IdRltdOrgTxblPrtnrshp_PrmryActvtsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_prdmnntincmtxt = models.CharField(db_column='IdRltdOrgTxblPrtnrshp_PrdmnntIncmTxt', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_shrofttlincmamt = models.BigIntegerField(db_column='IdRltdOrgTxblPrtnrshp_ShrOfTtlIncmAmt', blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_shrofeoyasstsamt = models.BigIntegerField(db_column='IdRltdOrgTxblPrtnrshp_ShrOfEOYAsstsAmt', blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_dsprprtntallctnsind = models.CharField(db_column='IdRltdOrgTxblPrtnrshp_DsprprtntAllctnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_ubicdvamt = models.BigIntegerField(db_column='IdRltdOrgTxblPrtnrshp_UBICdVAmt', blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_gnrlormngngprtnrind = models.CharField(db_column='IdRltdOrgTxblPrtnrshp_GnrlOrMngngPrtnrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_ownrshppct = models.DecimalField(db_column='IdRltdOrgTxblPrtnrshp_OwnrshpPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_lgldmclsttcd = models.CharField(db_column='IdRltdOrgTxblPrtnrshp_LglDmclSttCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_lgldmclfrgncntrycd = models.CharField(db_column='IdRltdOrgTxblPrtnrshp_LglDmclFrgnCntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    drctcntrllngenttynm_bsnssnmln1txt = models.CharField(db_column='DrctCntrllngEnttyNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    drctcntrllngenttynm_bsnssnmln2txt = models.CharField(db_column='DrctCntrllngEnttyNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    idrltdorgtxblprtnrshp_drctcntrllngnacd = models.TextField(db_column='IdRltdOrgTxblPrtnrshp_DrctCntrllngNACd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdridrltdorgtxblprtnrshp'


class ReturnSkdridrltdtxexmptorg(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdr_idrltdtxexmptorg = models.TextField(db_column='SkdR_IdRltdTxExmptOrg', blank=True, null=True)  # Field name made lowercase.
    dsrgrddenttynm_bsnssnmln1txt = models.CharField(db_column='DsrgrddEnttyNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    dsrgrddenttynm_bsnssnmln2txt = models.CharField(db_column='DsrgrddEnttyNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    idrltdtxexmptorg_ein = models.CharField(db_column='IdRltdTxExmptOrg_EIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    idrltdtxexmptorg_prmryactvtstxt = models.CharField(db_column='IdRltdTxExmptOrg_PrmryActvtsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    idrltdtxexmptorg_exmptcdsctntxt = models.CharField(db_column='IdRltdTxExmptOrg_ExmptCdSctnTxt', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idrltdtxexmptorg_pblcchrtysttstxt = models.CharField(db_column='IdRltdTxExmptOrg_PblcChrtySttsTxt', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idrltdtxexmptorg_cntrlldorgnztnind = models.CharField(db_column='IdRltdTxExmptOrg_CntrlldOrgnztnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    idrltdtxexmptorg_lgldmclsttcd = models.CharField(db_column='IdRltdTxExmptOrg_LglDmclSttCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    idrltdtxexmptorg_lgldmclfrgncntrycd = models.CharField(db_column='IdRltdTxExmptOrg_LglDmclFrgnCntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    drctcntrllngenttynm_bsnssnmln1txt = models.CharField(db_column='DrctCntrllngEnttyNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    drctcntrllngenttynm_bsnssnmln2txt = models.CharField(db_column='DrctCntrllngEnttyNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    idrltdtxexmptorg_drctcntrllngnacd = models.TextField(db_column='IdRltdTxExmptOrg_DrctCntrllngNACd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdridrltdtxexmptorg'


class ReturnSkdrspplmntlinfrmtndtl(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spplmntlinfrmtndtl = models.TextField(db_column='SpplmntlInfrmtnDtl', blank=True, null=True)  # Field name made lowercase.
    frmandlnrfrncdsc = models.CharField(db_column='FrmAndLnRfrncDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    explntntxt = models.TextField(db_column='ExplntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdrspplmntlinfrmtndtl'


class ReturnSkdrtrnsctnsrltdorg(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    bsnssnmln1txt = models.CharField(db_column='BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnmln2txt = models.CharField(db_column='BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    trnsctntxt = models.TextField(db_column='TrnsctnTxt', blank=True, null=True)  # Field name made lowercase.
    invlvdamt = models.BigIntegerField(db_column='InvlvdAmt', blank=True, null=True)  # Field name made lowercase.
    mthdofamntdtrmntntxt = models.TextField(db_column='MthdOfAmntDtrmntnTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdrtrnsctnsrltdorg'


class ReturnSkdrunrltdorgtxblprtnrshp(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdr_unrltdorgtxblprtnrshp = models.TextField(db_column='SkdR_UnrltdOrgTxblPrtnrshp', blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln1txt = models.CharField(db_column='BsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    bsnssnm_bsnssnmln2txt = models.CharField(db_column='BsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_ein = models.CharField(db_column='UnrltdOrgTxblPrtnrshp_EIN', max_length=9, blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_prmryactvtstxt = models.CharField(db_column='UnrltdOrgTxblPrtnrshp_PrmryActvtsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_prdmntincmdsc = models.TextField(db_column='UnrltdOrgTxblPrtnrshp_PrdmntIncmDsc', blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_allprtnrsc3sind = models.CharField(db_column='UnrltdOrgTxblPrtnrshp_AllPrtnrsC3SInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_shrofttlincmamt = models.BigIntegerField(db_column='UnrltdOrgTxblPrtnrshp_ShrOfTtlIncmAmt', blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_shrofeoyasstsamt = models.BigIntegerField(db_column='UnrltdOrgTxblPrtnrshp_ShrOfEOYAsstsAmt', blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_dsprprtntallctnsind = models.CharField(db_column='UnrltdOrgTxblPrtnrshp_DsprprtntAllctnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_ubicdvamt = models.BigIntegerField(db_column='UnrltdOrgTxblPrtnrshp_UBICdVAmt', blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_gnrlormngngprtnrind = models.CharField(db_column='UnrltdOrgTxblPrtnrshp_GnrlOrMngngPrtnrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_ownrshppct = models.DecimalField(db_column='UnrltdOrgTxblPrtnrshp_OwnrshpPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln1txt = models.CharField(db_column='USAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_addrssln2txt = models.CharField(db_column='USAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    usaddrss_ctynm = models.CharField(db_column='USAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    usaddrss_sttabbrvtncd = models.CharField(db_column='USAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usaddrss_zipcd = models.CharField(db_column='USAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln1txt = models.CharField(db_column='FrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_addrssln2txt = models.CharField(db_column='FrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_ctynm = models.TextField(db_column='FrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_prvncorsttnm = models.TextField(db_column='FrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_cntrycd = models.CharField(db_column='FrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    frgnaddrss_frgnpstlcd = models.TextField(db_column='FrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_lgldmclsttcd = models.CharField(db_column='UnrltdOrgTxblPrtnrshp_LglDmclSttCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    unrltdorgtxblprtnrshp_lgldmclfrgncntrycd = models.CharField(db_column='UnrltdOrgTxblPrtnrshp_LglDmclFrgnCntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skdrunrltdorgtxblprtnrshp'


class ReturnSkedaPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    chrchind = models.CharField(db_column='ChrchInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    schlind = models.CharField(db_column='SchlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hsptlind = models.CharField(db_column='HsptlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cllgorgnztnind = models.CharField(db_column='CllgOrgnztnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gvrnmntluntind = models.CharField(db_column='GvrnmntlUntInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pblcorgnztn170ind = models.CharField(db_column='PblcOrgnztn170Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cmmntytrstind = models.CharField(db_column='CmmntyTrstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pblclyspprtdorg5092ind = models.CharField(db_column='PblclySpprtdOrg5092Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tstpblcsftyind = models.CharField(db_column='TstPblcSftyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mdclrsrchorgnztnind = models.CharField(db_column='MdclRsrchOrgnztnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    agrcltrlrsrchorgind = models.CharField(db_column='AgrcltrlRsrchOrgInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    spprtngorgnztn5093ind = models.CharField(db_column='SpprtngOrgnztn5093Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    spprtngorg1ind = models.CharField(db_column='SpprtngOrg1Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    spprtngorg2ind = models.CharField(db_column='SpprtngOrg2Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    spprtngorg3fncintind = models.CharField(db_column='SpprtngOrg3FncIntInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    spprtngorg3nnfncind = models.CharField(db_column='SpprtngOrg3NnFncInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    irswrttndtrmntnind = models.CharField(db_column='IRSWrttnDtrmntnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    spprtdorgnztnscnt = models.BigIntegerField(db_column='SpprtdOrgnztnsCnt', blank=True, null=True)  # Field name made lowercase.
    spprtdorgnztnsttlcnt = models.BigIntegerField(db_column='SpprtdOrgnztnsTtlCnt', blank=True, null=True)  # Field name made lowercase.
    othrspprtsmamt = models.BigIntegerField(db_column='OthrSpprtSmAmt', blank=True, null=True)  # Field name made lowercase.
    spprtsmamt = models.BigIntegerField(db_column='SpprtSmAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skeda_part_i'


class ReturnSkedaPartIi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    gftsgrntscntrrcvd170_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='GftsGrntsCntrRcvd170_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gftsgrntscntrrcvd170_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='GftsGrntsCntrRcvd170_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gftsgrntscntrrcvd170_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='GftsGrntsCntrRcvd170_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gftsgrntscntrrcvd170_crrnttxyrmns1yramt = models.BigIntegerField(db_column='GftsGrntsCntrRcvd170_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    gftsgrntscntrrcvd170_crrnttxyramt = models.BigIntegerField(db_column='GftsGrntsCntrRcvd170_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    gftsgrntscntrrcvd170_ttlamt = models.BigIntegerField(db_column='GftsGrntsCntrRcvd170_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft170_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft170_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft170_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft170_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft170_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft170_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft170_crrnttxyrmns1yramt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft170_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft170_crrnttxyramt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft170_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft170_ttlamt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft170_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl170_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl170_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl170_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl170_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl170_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl170_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl170_crrnttxyrmns1yramt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl170_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl170_crrnttxyramt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl170_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl170_ttlamt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl170_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlclndryr170_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='TtlClndrYr170_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlclndryr170_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='TtlClndrYr170_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlclndryr170_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='TtlClndrYr170_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlclndryr170_crrnttxyrmns1yramt = models.BigIntegerField(db_column='TtlClndrYr170_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlclndryr170_crrnttxyramt = models.BigIntegerField(db_column='TtlClndrYr170_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlclndryr170_ttlamt = models.BigIntegerField(db_column='TtlClndrYr170_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    skda_sbstntlcntrbtrsttamt = models.BigIntegerField(db_column='SkdA_SbstntlCntrbtrsTtAmt', blank=True, null=True)  # Field name made lowercase.
    skda_pblcspprtttl170amt = models.BigIntegerField(db_column='SkdA_PblcSpprtTtl170Amt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm170_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='GrssInvstmntIncm170_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm170_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='GrssInvstmntIncm170_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm170_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='GrssInvstmntIncm170_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm170_crrnttxyrmns1yramt = models.BigIntegerField(db_column='GrssInvstmntIncm170_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm170_crrnttxyramt = models.BigIntegerField(db_column='GrssInvstmntIncm170_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm170_ttlamt = models.BigIntegerField(db_column='GrssInvstmntIncm170_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    unrltdbsnssntincm170_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='UnrltdBsnssNtIncm170_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    unrltdbsnssntincm170_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='UnrltdBsnssNtIncm170_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    unrltdbsnssntincm170_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='UnrltdBsnssNtIncm170_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    unrltdbsnssntincm170_crrnttxyrmns1yramt = models.BigIntegerField(db_column='UnrltdBsnssNtIncm170_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    unrltdbsnssntincm170_crrnttxyramt = models.BigIntegerField(db_column='UnrltdBsnssNtIncm170_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    unrltdbsnssntincm170_ttlamt = models.BigIntegerField(db_column='UnrltdBsnssNtIncm170_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm170_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='OthrIncm170_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm170_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='OthrIncm170_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm170_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='OthrIncm170_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm170_crrnttxyrmns1yramt = models.BigIntegerField(db_column='OthrIncm170_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm170_crrnttxyramt = models.BigIntegerField(db_column='OthrIncm170_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm170_ttlamt = models.BigIntegerField(db_column='OthrIncm170_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    skda_ttlspprtamt = models.BigIntegerField(db_column='SkdA_TtlSpprtAmt', blank=True, null=True)  # Field name made lowercase.
    skda_grssrcptsrltdactvtsamt = models.BigIntegerField(db_column='SkdA_GrssRcptsRltdActvtsAmt', blank=True, null=True)  # Field name made lowercase.
    skda_frst5yrs170ind = models.CharField(db_column='SkdA_Frst5Yrs170Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skda_pblcspprtcy170pct = models.DecimalField(db_column='SkdA_PblcSpprtCY170Pct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skda_pblcspprtpy170pct = models.DecimalField(db_column='SkdA_PblcSpprtPY170Pct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skda_thrtythrpctsprttstscy170ind = models.CharField(db_column='SkdA_ThrtyThrPctSprtTstsCY170Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skda_thrtythrpctsprttstspy170ind = models.CharField(db_column='SkdA_ThrtyThrPctSprtTstsPY170Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skda_tnpctfctscrcmstncststcyind = models.CharField(db_column='SkdA_TnPctFctsCrcmstncsTstCYInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skda_tnpctfctscrcmstncststpyind = models.CharField(db_column='SkdA_TnPctFctsCrcmstncsTstPYInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skda_prvtfndtn170ind = models.CharField(db_column='SkdA_PrvtFndtn170Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skeda_part_ii'


class ReturnSkedaPartIii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    gftsgrntscntrsrcvd509_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='GftsGrntsCntrsRcvd509_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gftsgrntscntrsrcvd509_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='GftsGrntsCntrsRcvd509_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gftsgrntscntrsrcvd509_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='GftsGrntsCntrsRcvd509_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gftsgrntscntrsrcvd509_crrnttxyrmns1yramt = models.BigIntegerField(db_column='GftsGrntsCntrsRcvd509_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    gftsgrntscntrsrcvd509_crrnttxyramt = models.BigIntegerField(db_column='GftsGrntsCntrsRcvd509_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    gftsgrntscntrsrcvd509_ttlamt = models.BigIntegerField(db_column='GftsGrntsCntrsRcvd509_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsadmssns_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='GrssRcptsAdmssns_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsadmssns_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='GrssRcptsAdmssns_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsadmssns_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='GrssRcptsAdmssns_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsadmssns_crrnttxyrmns1yramt = models.BigIntegerField(db_column='GrssRcptsAdmssns_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsadmssns_crrnttxyramt = models.BigIntegerField(db_column='GrssRcptsAdmssns_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsadmssns_ttlamt = models.BigIntegerField(db_column='GrssRcptsAdmssns_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsnnunrltbs_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='GrssRcptsNnUnrltBs_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsnnunrltbs_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='GrssRcptsNnUnrltBs_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsnnunrltbs_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='GrssRcptsNnUnrltBs_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsnnunrltbs_crrnttxyrmns1yramt = models.BigIntegerField(db_column='GrssRcptsNnUnrltBs_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsnnunrltbs_crrnttxyramt = models.BigIntegerField(db_column='GrssRcptsNnUnrltBs_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsnnunrltbs_ttlamt = models.BigIntegerField(db_column='GrssRcptsNnUnrltBs_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft509_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft509_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft509_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft509_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft509_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft509_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft509_crrnttxyrmns1yramt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft509_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft509_crrnttxyramt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft509_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    txrvlvdorgnztnlbnft509_ttlamt = models.BigIntegerField(db_column='TxRvLvdOrgnztnlBnft509_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl509_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl509_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl509_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl509_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl509_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl509_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl509_crrnttxyrmns1yramt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl509_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl509_crrnttxyramt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl509_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    gvtfrnsrvcfcltsvl509_ttlamt = models.BigIntegerField(db_column='GvtFrnSrvcFcltsVl509_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttl509_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='Ttl509_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ttl509_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='Ttl509_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ttl509_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='Ttl509_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ttl509_crrnttxyrmns1yramt = models.BigIntegerField(db_column='Ttl509_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    ttl509_crrnttxyramt = models.BigIntegerField(db_column='Ttl509_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttl509_ttlamt = models.BigIntegerField(db_column='Ttl509_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    amntsrcvddsqlfyprsn_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='AmntsRcvdDsqlfyPrsn_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    amntsrcvddsqlfyprsn_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='AmntsRcvdDsqlfyPrsn_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    amntsrcvddsqlfyprsn_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='AmntsRcvdDsqlfyPrsn_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    amntsrcvddsqlfyprsn_crrnttxyrmns1yramt = models.BigIntegerField(db_column='AmntsRcvdDsqlfyPrsn_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    amntsrcvddsqlfyprsn_crrnttxyramt = models.BigIntegerField(db_column='AmntsRcvdDsqlfyPrsn_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    amntsrcvddsqlfyprsn_ttlamt = models.BigIntegerField(db_column='AmntsRcvdDsqlfyPrsn_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    sbstntlcntrbtrsamt_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='SbstntlCntrbtrsAmt_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    sbstntlcntrbtrsamt_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='SbstntlCntrbtrsAmt_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    sbstntlcntrbtrsamt_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='SbstntlCntrbtrsAmt_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    sbstntlcntrbtrsamt_crrnttxyrmns1yramt = models.BigIntegerField(db_column='SbstntlCntrbtrsAmt_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    sbstntlcntrbtrsamt_crrnttxyramt = models.BigIntegerField(db_column='SbstntlCntrbtrsAmt_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    sbstntlcntrbtrsamt_ttlamt = models.BigIntegerField(db_column='SbstntlCntrbtrsAmt_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    sbstanddsqlfyprsnstt_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='SbstAndDsqlfyPrsnsTt_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    sbstanddsqlfyprsnstt_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='SbstAndDsqlfyPrsnsTt_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    sbstanddsqlfyprsnstt_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='SbstAndDsqlfyPrsnsTt_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    sbstanddsqlfyprsnstt_crrnttxyrmns1yramt = models.BigIntegerField(db_column='SbstAndDsqlfyPrsnsTt_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    sbstanddsqlfyprsnstt_crrnttxyramt = models.BigIntegerField(db_column='SbstAndDsqlfyPrsnsTt_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    sbstanddsqlfyprsnstt_ttlamt = models.BigIntegerField(db_column='SbstAndDsqlfyPrsnsTt_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    skda_pblcspprtttl509amt = models.BigIntegerField(db_column='SkdA_PblcSpprtTtl509Amt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm509_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='GrssInvstmntIncm509_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm509_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='GrssInvstmntIncm509_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm509_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='GrssInvstmntIncm509_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm509_crrnttxyrmns1yramt = models.BigIntegerField(db_column='GrssInvstmntIncm509_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm509_crrnttxyramt = models.BigIntegerField(db_column='GrssInvstmntIncm509_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    grssinvstmntincm509_ttlamt = models.BigIntegerField(db_column='GrssInvstmntIncm509_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    pst1975ubti_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='Pst1975UBTI_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    pst1975ubti_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='Pst1975UBTI_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    pst1975ubti_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='Pst1975UBTI_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    pst1975ubti_crrnttxyrmns1yramt = models.BigIntegerField(db_column='Pst1975UBTI_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    pst1975ubti_crrnttxyramt = models.BigIntegerField(db_column='Pst1975UBTI_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    pst1975ubti_ttlamt = models.BigIntegerField(db_column='Pst1975UBTI_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincmandubti_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='InvstmntIncmAndUBTI_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincmandubti_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='InvstmntIncmAndUBTI_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincmandubti_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='InvstmntIncmAndUBTI_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincmandubti_crrnttxyrmns1yramt = models.BigIntegerField(db_column='InvstmntIncmAndUBTI_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincmandubti_crrnttxyramt = models.BigIntegerField(db_column='InvstmntIncmAndUBTI_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntincmandubti_ttlamt = models.BigIntegerField(db_column='InvstmntIncmAndUBTI_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmothrubi_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='NtIncmFrmOthrUBI_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmothrubi_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='NtIncmFrmOthrUBI_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmothrubi_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='NtIncmFrmOthrUBI_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmothrubi_crrnttxyrmns1yramt = models.BigIntegerField(db_column='NtIncmFrmOthrUBI_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmothrubi_crrnttxyramt = models.BigIntegerField(db_column='NtIncmFrmOthrUBI_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmfrmothrubi_ttlamt = models.BigIntegerField(db_column='NtIncmFrmOthrUBI_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm509_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='OthrIncm509_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm509_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='OthrIncm509_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm509_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='OthrIncm509_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm509_crrnttxyrmns1yramt = models.BigIntegerField(db_column='OthrIncm509_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm509_crrnttxyramt = models.BigIntegerField(db_column='OthrIncm509_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    othrincm509_ttlamt = models.BigIntegerField(db_column='OthrIncm509_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlspprtclndryr_crrnttxyrmns4yrsamt = models.BigIntegerField(db_column='TtlSpprtClndrYr_CrrntTxYrMns4YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlspprtclndryr_crrnttxyrmns3yrsamt = models.BigIntegerField(db_column='TtlSpprtClndrYr_CrrntTxYrMns3YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlspprtclndryr_crrnttxyrmns2yrsamt = models.BigIntegerField(db_column='TtlSpprtClndrYr_CrrntTxYrMns2YrsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlspprtclndryr_crrnttxyrmns1yramt = models.BigIntegerField(db_column='TtlSpprtClndrYr_CrrntTxYrMns1YrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlspprtclndryr_crrnttxyramt = models.BigIntegerField(db_column='TtlSpprtClndrYr_CrrntTxYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlspprtclndryr_ttlamt = models.BigIntegerField(db_column='TtlSpprtClndrYr_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    skda_frst5yrs509ind = models.CharField(db_column='SkdA_Frst5Yrs509Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skda_pblcspprtcy509pct = models.DecimalField(db_column='SkdA_PblcSpprtCY509Pct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skda_pblcspprtpy509pct = models.DecimalField(db_column='SkdA_PblcSpprtPY509Pct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skda_invstmntincmcypct = models.DecimalField(db_column='SkdA_InvstmntIncmCYPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skda_invstmntincmpypct = models.DecimalField(db_column='SkdA_InvstmntIncmPYPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skda_thrtythrpctsprttstscy509ind = models.CharField(db_column='SkdA_ThrtyThrPctSprtTstsCY509Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skda_thrtythrpctsprttstspy509ind = models.CharField(db_column='SkdA_ThrtyThrPctSprtTstsPY509Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skda_prvtfndtn509ind = models.CharField(db_column='SkdA_PrvtFndtn509Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skeda_part_iii'


class ReturnSkedaPartIv(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    frm990schaspprtngorg = models.TextField(db_column='Frm990SchASpprtngOrg', blank=True, null=True)  # Field name made lowercase.
    lstdbynmgvrnngdcind = models.CharField(db_column='LstdByNmGvrnngDcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sprtorgnirsdtrmntnind = models.CharField(db_column='SprtOrgNIRSDtrmntnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    spprtdorgsctnc456ind = models.CharField(db_column='SpprtdOrgSctnC456Ind', max_length=5, blank=True, null=True)  # Field name made lowercase.
    spprtdorgqlfdind = models.CharField(db_column='SpprtdOrgQlfdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sprtexclsvlysc170c2bind = models.CharField(db_column='SprtExclsvlySc170c2BInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    spprtdorgntorgnzdusind = models.CharField(db_column='SpprtdOrgNtOrgnzdUSInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cntrldcdnggrntfrgnorgind = models.CharField(db_column='CntrlDcdngGrntFrgnOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    spprtfrgnorgndtrmind = models.CharField(db_column='SpprtFrgnOrgNDtrmInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    orgnztnchngsprtorgind = models.CharField(db_column='OrgnztnChngSprtOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    spprtdorgclssdsgntdind = models.CharField(db_column='SpprtdOrgClssDsgntdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sbstttnbyndorgcntlind = models.CharField(db_column='SbstttnByndOrgCntlInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    spprtnnspprtdorgind = models.CharField(db_column='SpprtNnSpprtdOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pymntsbstntlcntrbtrind = models.CharField(db_column='PymntSbstntlCntrbtrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lndsqlfdprsnind = models.CharField(db_column='LnDsqlfdPrsnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cntrllddsqlfdprsnind = models.CharField(db_column='CntrlldDsqlfdPrsnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dsqlfdprsncntrllintind = models.CharField(db_column='DsqlfdPrsnCntrllIntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dsqlfdprsnownrintind = models.CharField(db_column='DsqlfdPrsnOwnrIntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    excssbsnsshldngsrlsind = models.CharField(db_column='ExcssBsnssHldngsRlsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    excssbsnsshldngsind = models.CharField(db_column='ExcssBsnssHldngsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cntrbtncntrllrind = models.CharField(db_column='CntrbtnCntrllrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cntrbtnfmlyind = models.CharField(db_column='CntrbtnFmlyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cntrbtn35cntrlldind = models.CharField(db_column='Cntrbtn35CntrlldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm990scha1sprtorg = models.TextField(db_column='Frm990SchA1SprtOrg', blank=True, null=True)  # Field name made lowercase.
    pwrappntmjrtydrtrstind = models.CharField(db_column='PwrAppntMjrtyDrTrstInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    oprtbnftnnsprtorgind = models.CharField(db_column='OprtBnftNnSprtOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mjrtydrtrstspprtdorgind = models.CharField(db_column='MjrtyDrTrstSpprtdOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm990scha3sprtorgall = models.TextField(db_column='Frm990SchA3SprtOrgAll', blank=True, null=True)  # Field name made lowercase.
    tmlyprvdddcmntsind = models.CharField(db_column='TmlyPrvddDcmntsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    offcrsclsrltnshpind = models.CharField(db_column='OffcrsClsRltnshpInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    spprtdorgvcinvstmntind = models.CharField(db_column='SpprtdOrgVcInvstmntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frm990scha3fncint = models.TextField(db_column='Frm990SchA3FncInt', blank=True, null=True)  # Field name made lowercase.
    actvtststind = models.CharField(db_column='ActvtsTstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prntspprtdorgind = models.CharField(db_column='PrntSpprtdOrgInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gvrnmntlenttyind = models.CharField(db_column='GvrnmntlEnttyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    actvtsfrthrexmptprpsind = models.CharField(db_column='ActvtsFrthrExmptPrpsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    actvtsenggdorginvlmntind = models.CharField(db_column='ActvtsEnggdOrgInvlmntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    appntelctmjrtyoffcrind = models.CharField(db_column='AppntElctMjrtyOffcrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    exrcsdrctnplcsind = models.CharField(db_column='ExrcsDrctnPlcsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skeda_part_iv'


class ReturnSkedaPartV(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skda_trstintgrlprttstind = models.CharField(db_column='SkdA_TrstIntgrlPrtTstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skda_adjstdntincm = models.TextField(db_column='SkdA_AdjstdNtIncm', blank=True, null=True)  # Field name made lowercase.
    ntstcptlgnadjntincm_prryramt = models.BigIntegerField(db_column='NtSTCptlGnAdjNtIncm_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    ntstcptlgnadjntincm_crrntyramt = models.BigIntegerField(db_column='NtSTCptlGnAdjNtIncm_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    rcvrspydstrbtns_prryramt = models.BigIntegerField(db_column='RcvrsPYDstrbtns_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    rcvrspydstrbtns_crrntyramt = models.BigIntegerField(db_column='RcvrsPYDstrbtns_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    othrgrssincm_prryramt = models.BigIntegerField(db_column='OthrGrssIncm_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    othrgrssincm_crrntyramt = models.BigIntegerField(db_column='OthrGrssIncm_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    adjstdgrssincm_prryramt = models.BigIntegerField(db_column='AdjstdGrssIncm_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    adjstdgrssincm_crrntyramt = models.BigIntegerField(db_column='AdjstdGrssIncm_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    dprctndpltn_prryramt = models.BigIntegerField(db_column='DprctnDpltn_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    dprctndpltn_crrntyramt = models.BigIntegerField(db_column='DprctnDpltn_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    prdctnincm_prryramt = models.BigIntegerField(db_column='PrdctnIncm_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    prdctnincm_crrntyramt = models.BigIntegerField(db_column='PrdctnIncm_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    othrexpnss_prryramt = models.BigIntegerField(db_column='OthrExpnss_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    othrexpnss_crrntyramt = models.BigIntegerField(db_column='OthrExpnss_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttladjstdntincm_prryramt = models.BigIntegerField(db_column='TtlAdjstdNtIncm_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttladjstdntincm_crrntyramt = models.BigIntegerField(db_column='TtlAdjstdNtIncm_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    skda_mnmmasstamnt = models.TextField(db_column='SkdA_MnmmAsstAmnt', blank=True, null=True)  # Field name made lowercase.
    avrgmnthlyfmvofsc_prryramt = models.BigIntegerField(db_column='AvrgMnthlyFMVOfSc_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    avrgmnthlyfmvofsc_crrntyramt = models.BigIntegerField(db_column='AvrgMnthlyFMVOfSc_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    avrgmnthlycshblncs_prryramt = models.BigIntegerField(db_column='AvrgMnthlyCshBlncs_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    avrgmnthlycshblncs_crrntyramt = models.BigIntegerField(db_column='AvrgMnthlyCshBlncs_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    fmvothrnnexmptusasst_prryramt = models.BigIntegerField(db_column='FMVOthrNnExmptUsAsst_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    fmvothrnnexmptusasst_crrntyramt = models.BigIntegerField(db_column='FMVOthrNnExmptUsAsst_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlfmvofnnexmptusasst_prryramt = models.BigIntegerField(db_column='TtlFMVOfNnExmptUsAsst_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlfmvofnnexmptusasst_crrntyramt = models.BigIntegerField(db_column='TtlFMVOfNnExmptUsAsst_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    mnmmasstamnt_dscntclmdamt = models.BigIntegerField(db_column='MnmmAsstAmnt_DscntClmdAmt', blank=True, null=True)  # Field name made lowercase.
    acqstnindbtdnss_prryramt = models.BigIntegerField(db_column='AcqstnIndbtdnss_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    acqstnindbtdnss_crrntyramt = models.BigIntegerField(db_column='AcqstnIndbtdnss_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    adjstdfmvlssindbtdnss_prryramt = models.BigIntegerField(db_column='AdjstdFMVLssIndbtdnss_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    adjstdfmvlssindbtdnss_crrntyramt = models.BigIntegerField(db_column='AdjstdFMVLssIndbtdnss_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    cshdmdchrtbl_prryramt = models.BigIntegerField(db_column='CshDmdChrtbl_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    cshdmdchrtbl_crrntyramt = models.BigIntegerField(db_column='CshDmdChrtbl_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    ntvlnnexmptusassts_prryramt = models.BigIntegerField(db_column='NtVlNnExmptUsAssts_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    ntvlnnexmptusassts_crrntyramt = models.BigIntegerField(db_column='NtVlNnExmptUsAssts_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    pctofntvlnnexmptusast_prryramt = models.BigIntegerField(db_column='PctOfNtVlNnExmptUsAst_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    pctofntvlnnexmptusast_crrntyramt = models.BigIntegerField(db_column='PctOfNtVlNnExmptUsAst_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    rcvrspydstrmnasst_prryramt = models.BigIntegerField(db_column='RcvrsPYDstrMnAsst_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    rcvrspydstrmnasst_crrntyramt = models.BigIntegerField(db_column='RcvrsPYDstrMnAsst_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlmnmmasst_prryramt = models.BigIntegerField(db_column='TtlMnmmAsst_PrrYrAmt', blank=True, null=True)  # Field name made lowercase.
    ttlmnmmasst_crrntyramt = models.BigIntegerField(db_column='TtlMnmmAsst_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    skda_dstrbtblamnt = models.TextField(db_column='SkdA_DstrbtblAmnt', blank=True, null=True)  # Field name made lowercase.
    dstrbtblamnt_cyadjntincmdstrbtblamt = models.BigIntegerField(db_column='DstrbtblAmnt_CYAdjNtIncmDstrbtblAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtblamnt_cypct85adjstdntincmamt = models.BigIntegerField(db_column='DstrbtblAmnt_CYPct85AdjstdNtIncmAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtblamnt_cyttlmnastdstrbtblamt = models.BigIntegerField(db_column='DstrbtblAmnt_CYTtlMnAstDstrbtblAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtblamnt_cygrtradjstdmnmmamt = models.BigIntegerField(db_column='DstrbtblAmnt_CYGrtrAdjstdMnmmAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtblamnt_cyincmtximpsdpyamt = models.BigIntegerField(db_column='DstrbtblAmnt_CYIncmTxImpsdPYAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtblamnt_cydstrbtblasadjstdamt = models.BigIntegerField(db_column='DstrbtblAmnt_CYDstrbtblAsAdjstdAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtblamnt_frstyr3nnfncind = models.CharField(db_column='DstrbtblAmnt_FrstYr3NnFncInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skda_dstrbtns = models.TextField(db_column='SkdA_Dstrbtns', blank=True, null=True)  # Field name made lowercase.
    dstrbtns_cypdaccmplshexmptprpsamt = models.BigIntegerField(db_column='Dstrbtns_CYPdAccmplshExmptPrpsAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtns_cypdinexcssincmactvtyamt = models.BigIntegerField(db_column='Dstrbtns_CYPdInExcssIncmActvtyAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtns_cyadmnstrtvexpnspdamt = models.BigIntegerField(db_column='Dstrbtns_CYAdmnstrtvExpnsPdAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtns_exmptusasstsacqspdamt = models.BigIntegerField(db_column='Dstrbtns_ExmptUsAsstsAcqsPdAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtns_qlfdstasdamt = models.BigIntegerField(db_column='Dstrbtns_QlfdStAsdAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtns_cyothrdstrbtnsamt = models.BigIntegerField(db_column='Dstrbtns_CYOthrDstrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtns_cyttlannldstrbtnsamt = models.BigIntegerField(db_column='Dstrbtns_CYTtlAnnlDstrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtns_cydstrattntvsprtorgamt = models.BigIntegerField(db_column='Dstrbtns_CYDstrAttntvSprtOrgAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtns_cydstrbtblasadjstdamt = models.BigIntegerField(db_column='Dstrbtns_CYDstrbtblAsAdjstdAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtns_cydstrbtnyrrt = models.TextField(db_column='Dstrbtns_CYDstrbtnYrRt', blank=True, null=True)  # Field name made lowercase.
    skda_dstrbtnallctns = models.TextField(db_column='SkdA_DstrbtnAllctns', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_cydstrbtblasadjstdamt = models.BigIntegerField(db_column='DstrbtnAllctns_CYDstrbtblAsAdjstdAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_undrdstrbtnsamt = models.BigIntegerField(db_column='DstrbtnAllctns_UndrdstrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_excssdstrbtncyvyr3amt = models.BigIntegerField(db_column='DstrbtnAllctns_ExcssDstrbtnCyvYr3Amt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_excssdstrbtncyvyr2amt = models.BigIntegerField(db_column='DstrbtnAllctns_ExcssDstrbtnCyvYr2Amt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_excssdstrbtncyvyr1amt = models.BigIntegerField(db_column='DstrbtnAllctns_ExcssDstrbtnCyvYr1Amt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_ttlexcssdstrbtncyvamt = models.BigIntegerField(db_column='DstrbtnAllctns_TtlExcssDstrbtnCyvAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_cyvappldundrdstrpyamt = models.BigIntegerField(db_column='DstrbtnAllctns_CyvAppldUndrdstrPYAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_cyvappldundrdstrcpyamt = models.BigIntegerField(db_column='DstrbtnAllctns_CyvAppldUndrdstrCPYAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_excssdstrbtncyvamt = models.BigIntegerField(db_column='DstrbtnAllctns_ExcssDstrbtnCyvAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_cyttlannldstrbtnsamt = models.BigIntegerField(db_column='DstrbtnAllctns_CYTtlAnnlDstrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_cydstrbappundrdstrpyamt = models.BigIntegerField(db_column='DstrbtnAllctns_CYDstrbAppUndrdstrPYAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_cydstrappdstrbtblamt = models.BigIntegerField(db_column='DstrbtnAllctns_CYDstrAppDstrbtblAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_excssdstrbtnamt = models.BigIntegerField(db_column='DstrbtnAllctns_ExcssDstrbtnAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_rmnngundrdstrpyamt = models.BigIntegerField(db_column='DstrbtnAllctns_RmnngUndrdstrPYAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_rmnngundrdstrcyamt = models.BigIntegerField(db_column='DstrbtnAllctns_RmnngUndrdstrCYAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_excssdstrcyvtnxtyramt = models.BigIntegerField(db_column='DstrbtnAllctns_ExcssDstrCyvTNxtYrAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_excssfrmyr4amt = models.BigIntegerField(db_column='DstrbtnAllctns_ExcssFrmYr4Amt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_excssfrmyr3amt = models.BigIntegerField(db_column='DstrbtnAllctns_ExcssFrmYr3Amt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_excssfrmyr2amt = models.BigIntegerField(db_column='DstrbtnAllctns_ExcssFrmYr2Amt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnallctns_excssfrmyr1amt = models.BigIntegerField(db_column='DstrbtnAllctns_ExcssFrmYr1Amt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skeda_part_v'


class ReturnSkedaPartVi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    fctsandcrcmstncststtxt = models.TextField(db_column='FctsAndCrcmstncsTstTxt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skeda_part_vi'


class ReturnSkedbPart0(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    orgnztn501cind = models.TextField(db_column='Orgnztn501cInd', blank=True, null=True)  # Field name made lowercase.
    orgnztn49471ntpfind = models.CharField(db_column='Orgnztn49471NtPFInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    orgnztn527ind = models.CharField(db_column='Orgnztn527Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    orgnztn501c3exmptpfind = models.CharField(db_column='Orgnztn501c3ExmptPFInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    orgnztn49471trtdpfind = models.CharField(db_column='Orgnztn49471TrtdPFInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    orgnztn501c3txblpfind = models.CharField(db_column='Orgnztn501c3TxblPFInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gnrlrlind = models.CharField(db_column='GnrlRlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    spclrlmton3rdsprttstind = models.CharField(db_column='SpclRlMtOn3rdSprtTstInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ttcntrrcvdmr1000ind = models.CharField(db_column='TtCntrRcvdMr1000Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ttcntrrcvdupt1000ind = models.TextField(db_column='TtCntrRcvdUpT1000Ind', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedb_part_0'


class ReturnSkedbPartIi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    ttlundr1000cntrbtnsamt = models.BigIntegerField(db_column='TtlUndr1000CntrbtnsAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedb_part_ii'


class ReturnSkedcPart0(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    pltclexpndtrsamt = models.BigIntegerField(db_column='PltclExpndtrsAmt', blank=True, null=True)  # Field name made lowercase.
    vlntrhrscnt = models.BigIntegerField(db_column='VlntrHrsCnt', blank=True, null=True)  # Field name made lowercase.
    sctn4955orgnztntxamt = models.BigIntegerField(db_column='Sctn4955OrgnztnTxAmt', blank=True, null=True)  # Field name made lowercase.
    sctn4955mngrstxamt = models.BigIntegerField(db_column='Sctn4955MngrsTxAmt', blank=True, null=True)  # Field name made lowercase.
    frm4720fldsctn4955txind = models.CharField(db_column='Frm4720FldSctn4955TxInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    crrctnmdind = models.CharField(db_column='CrrctnMdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    expndd527actvtsamt = models.BigIntegerField(db_column='Expndd527ActvtsAmt', blank=True, null=True)  # Field name made lowercase.
    intrnlfndscntrbtdamt = models.BigIntegerField(db_column='IntrnlFndsCntrbtdAmt', blank=True, null=True)  # Field name made lowercase.
    ttlexmptfnctnexpndamt = models.BigIntegerField(db_column='TtlExmptFnctnExpndAmt', blank=True, null=True)  # Field name made lowercase.
    frm1120polfldind = models.CharField(db_column='Frm1120POLFldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedc_part_0'


class ReturnSkedcPartIia(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdc_orgnztnblngsaffltind = models.TextField(db_column='SkdC_OrgnztnBlngsAffltInd', blank=True, null=True)  # Field name made lowercase.
    skdc_lmtdcntrlprvsnsappind = models.CharField(db_column='SkdC_LmtdCntrlPrvsnsAppInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ttlgrssrtslbbyng_flngorgnztnsttlamt = models.BigIntegerField(db_column='TtlGrssrtsLbbyng_FlngOrgnztnsTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlgrssrtslbbyng_affltdgrpttlamt = models.BigIntegerField(db_column='TtlGrssrtsLbbyng_AffltdGrpTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttldrctlbbyng_flngorgnztnsttlamt = models.BigIntegerField(db_column='TtlDrctLbbyng_FlngOrgnztnsTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttldrctlbbyng_affltdgrpttlamt = models.BigIntegerField(db_column='TtlDrctLbbyng_AffltdGrpTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttllbbyngexpnd_flngorgnztnsttlamt = models.BigIntegerField(db_column='TtlLbbyngExpnd_FlngOrgnztnsTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttllbbyngexpnd_affltdgrpttlamt = models.BigIntegerField(db_column='TtlLbbyngExpnd_AffltdGrpTtlAmt', blank=True, null=True)  # Field name made lowercase.
    othrexmptprpsexpnd_flngorgnztnsttlamt = models.BigIntegerField(db_column='OthrExmptPrpsExpnd_FlngOrgnztnsTtlAmt', blank=True, null=True)  # Field name made lowercase.
    othrexmptprpsexpnd_affltdgrpttlamt = models.BigIntegerField(db_column='OthrExmptPrpsExpnd_AffltdGrpTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlexmptprpsexpnd_flngorgnztnsttlamt = models.BigIntegerField(db_column='TtlExmptPrpsExpnd_FlngOrgnztnsTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlexmptprpsexpnd_affltdgrpttlamt = models.BigIntegerField(db_column='TtlExmptPrpsExpnd_AffltdGrpTtlAmt', blank=True, null=True)  # Field name made lowercase.
    lbbyngnntxblamnt_flngorgnztnsttlamt = models.BigIntegerField(db_column='LbbyngNntxblAmnt_FlngOrgnztnsTtlAmt', blank=True, null=True)  # Field name made lowercase.
    lbbyngnntxblamnt_affltdgrpttlamt = models.BigIntegerField(db_column='LbbyngNntxblAmnt_AffltdGrpTtlAmt', blank=True, null=True)  # Field name made lowercase.
    grssrtsnntxbl_flngorgnztnsttlamt = models.BigIntegerField(db_column='GrssrtsNntxbl_FlngOrgnztnsTtlAmt', blank=True, null=True)  # Field name made lowercase.
    grssrtsnntxbl_affltdgrpttlamt = models.BigIntegerField(db_column='GrssrtsNntxbl_AffltdGrpTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlbbynggrssrtmnsnntx_flngorgnztnsttlamt = models.BigIntegerField(db_column='TtLbbyngGrssrtMnsNnTx_FlngOrgnztnsTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlbbynggrssrtmnsnntx_affltdgrpttlamt = models.BigIntegerField(db_column='TtLbbyngGrssrtMnsNnTx_AffltdGrpTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlbbyexpndmnslbbyngnntx_flngorgnztnsttlamt = models.BigIntegerField(db_column='TtLbbyExpndMnsLbbyngNnTx_FlngOrgnztnsTtlAmt', blank=True, null=True)  # Field name made lowercase.
    ttlbbyexpndmnslbbyngnntx_affltdgrpttlamt = models.BigIntegerField(db_column='TtLbbyExpndMnsLbbyngNnTx_AffltdGrpTtlAmt', blank=True, null=True)  # Field name made lowercase.
    skdc_frm4720fldind = models.CharField(db_column='SkdC_Frm4720FldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    avglbbyngnntxblamnt_crrntyrmns3amt = models.BigIntegerField(db_column='AvgLbbyngNntxblAmnt_CrrntYrMns3Amt', blank=True, null=True)  # Field name made lowercase.
    avglbbyngnntxblamnt_crrntyrmns2amt = models.BigIntegerField(db_column='AvgLbbyngNntxblAmnt_CrrntYrMns2Amt', blank=True, null=True)  # Field name made lowercase.
    avglbbyngnntxblamnt_crrntyrmns1amt = models.BigIntegerField(db_column='AvgLbbyngNntxblAmnt_CrrntYrMns1Amt', blank=True, null=True)  # Field name made lowercase.
    avglbbyngnntxblamnt_crrntyramt = models.BigIntegerField(db_column='AvgLbbyngNntxblAmnt_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    avglbbyngnntxblamnt_ttlamt = models.BigIntegerField(db_column='AvgLbbyngNntxblAmnt_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    skdc_lbbyngclngamt = models.BigIntegerField(db_column='SkdC_LbbyngClngAmt', blank=True, null=True)  # Field name made lowercase.
    avgttllbbyngexpnd_crrntyrmns3amt = models.BigIntegerField(db_column='AvgTtlLbbyngExpnd_CrrntYrMns3Amt', blank=True, null=True)  # Field name made lowercase.
    avgttllbbyngexpnd_crrntyrmns2amt = models.BigIntegerField(db_column='AvgTtlLbbyngExpnd_CrrntYrMns2Amt', blank=True, null=True)  # Field name made lowercase.
    avgttllbbyngexpnd_crrntyrmns1amt = models.BigIntegerField(db_column='AvgTtlLbbyngExpnd_CrrntYrMns1Amt', blank=True, null=True)  # Field name made lowercase.
    avgttllbbyngexpnd_crrntyramt = models.BigIntegerField(db_column='AvgTtlLbbyngExpnd_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    avgttllbbyngexpnd_ttlamt = models.BigIntegerField(db_column='AvgTtlLbbyngExpnd_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    avggrssrtsnntxbl_crrntyrmns3amt = models.BigIntegerField(db_column='AvgGrssrtsNntxbl_CrrntYrMns3Amt', blank=True, null=True)  # Field name made lowercase.
    avggrssrtsnntxbl_crrntyrmns2amt = models.BigIntegerField(db_column='AvgGrssrtsNntxbl_CrrntYrMns2Amt', blank=True, null=True)  # Field name made lowercase.
    avggrssrtsnntxbl_crrntyrmns1amt = models.BigIntegerField(db_column='AvgGrssrtsNntxbl_CrrntYrMns1Amt', blank=True, null=True)  # Field name made lowercase.
    avggrssrtsnntxbl_crrntyramt = models.BigIntegerField(db_column='AvgGrssrtsNntxbl_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    avggrssrtsnntxbl_ttlamt = models.BigIntegerField(db_column='AvgGrssrtsNntxbl_TtlAmt', blank=True, null=True)  # Field name made lowercase.
    skdc_grssrtsclngamt = models.BigIntegerField(db_column='SkdC_GrssrtsClngAmt', blank=True, null=True)  # Field name made lowercase.
    avggrssrtslbbyngexpnd_crrntyrmns3amt = models.BigIntegerField(db_column='AvgGrssrtsLbbyngExpnd_CrrntYrMns3Amt', blank=True, null=True)  # Field name made lowercase.
    avggrssrtslbbyngexpnd_crrntyrmns2amt = models.BigIntegerField(db_column='AvgGrssrtsLbbyngExpnd_CrrntYrMns2Amt', blank=True, null=True)  # Field name made lowercase.
    avggrssrtslbbyngexpnd_crrntyrmns1amt = models.BigIntegerField(db_column='AvgGrssrtsLbbyngExpnd_CrrntYrMns1Amt', blank=True, null=True)  # Field name made lowercase.
    avggrssrtslbbyngexpnd_crrntyramt = models.BigIntegerField(db_column='AvgGrssrtsLbbyngExpnd_CrrntYrAmt', blank=True, null=True)  # Field name made lowercase.
    avggrssrtslbbyngexpnd_ttlamt = models.BigIntegerField(db_column='AvgGrssrtsLbbyngExpnd_TtlAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedc_part_iia'


class ReturnSkedcPartIib(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    vlntrsind = models.CharField(db_column='VlntrsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pdstfformngmntind = models.CharField(db_column='PdStffOrMngmntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mdadvrtsmntsind = models.CharField(db_column='MdAdvrtsmntsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mdadvrtsmntsamt = models.BigIntegerField(db_column='MdAdvrtsmntsAmt', blank=True, null=True)  # Field name made lowercase.
    mlngsmmbrsind = models.CharField(db_column='MlngsMmbrsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mlngsmmbrsamt = models.BigIntegerField(db_column='MlngsMmbrsAmt', blank=True, null=True)  # Field name made lowercase.
    pblctnsorbrdcstind = models.CharField(db_column='PblctnsOrBrdcstInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pblctnsorbrdcstamt = models.BigIntegerField(db_column='PblctnsOrBrdcstAmt', blank=True, null=True)  # Field name made lowercase.
    grntsothrorgnztnsind = models.CharField(db_column='GrntsOthrOrgnztnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    grntsothrorgnztnsamt = models.BigIntegerField(db_column='GrntsOthrOrgnztnsAmt', blank=True, null=True)  # Field name made lowercase.
    drctcntctlgsltrsind = models.CharField(db_column='DrctCntctLgsltrsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    drctcntctlgsltrsamt = models.BigIntegerField(db_column='DrctCntctLgsltrsAmt', blank=True, null=True)  # Field name made lowercase.
    rllsdmnstrtnsind = models.CharField(db_column='RllsDmnstrtnsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rllsdmnstrtnsamt = models.BigIntegerField(db_column='RllsDmnstrtnsAmt', blank=True, null=True)  # Field name made lowercase.
    othractvtsind = models.CharField(db_column='OthrActvtsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    othractvtsamt = models.BigIntegerField(db_column='OthrActvtsAmt', blank=True, null=True)  # Field name made lowercase.
    ttllbbyngexpndtrsamt = models.BigIntegerField(db_column='TtlLbbyngExpndtrsAmt', blank=True, null=True)  # Field name made lowercase.
    ntdscrbdsctn501c3ind = models.CharField(db_column='NtDscrbdSctn501c3Ind', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tx4912amt = models.BigIntegerField(db_column='Tx4912Amt', blank=True, null=True)  # Field name made lowercase.
    mngrs4912txamt = models.BigIntegerField(db_column='Mngrs4912TxAmt', blank=True, null=True)  # Field name made lowercase.
    frm4720fld4912txind = models.CharField(db_column='Frm4720Fld4912TxInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedc_part_iib'


class ReturnSkedcPartIiia(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    sbstntllyalldsnnddind = models.CharField(db_column='SbstntllyAllDsNnddInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    onlyinhslbbyngind = models.CharField(db_column='OnlyInHsLbbyngInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    agrcrryvrprryrind = models.CharField(db_column='AgrCrryvrPrrYrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedc_part_iiia'


class ReturnSkedcPartIiib(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dsassssmntsamt = models.BigIntegerField(db_column='DsAssssmntsAmt', blank=True, null=True)  # Field name made lowercase.
    nnddctbllbbyngpltclcyamt = models.BigIntegerField(db_column='NnDdctblLbbyngPltclCYAmt', blank=True, null=True)  # Field name made lowercase.
    nnddlbbyngpltclcyvamt = models.BigIntegerField(db_column='NnDdLbbyngPltclCyvAmt', blank=True, null=True)  # Field name made lowercase.
    nnddctbllbbyngpltclttamt = models.BigIntegerField(db_column='NnDdctblLbbyngPltclTtAmt', blank=True, null=True)  # Field name made lowercase.
    aggrgtrprtddsntcamt = models.BigIntegerField(db_column='AggrgtRprtdDsNtcAmt', blank=True, null=True)  # Field name made lowercase.
    crrdovramt = models.BigIntegerField(db_column='CrrdOvrAmt', blank=True, null=True)  # Field name made lowercase.
    txblamt = models.BigIntegerField(db_column='TxblAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedc_part_iiib'


class ReturnSkeddPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    dnradvsdfndshldcnt = models.BigIntegerField(db_column='DnrAdvsdFndsHldCnt', blank=True, null=True)  # Field name made lowercase.
    fndsandothraccntshldcnt = models.BigIntegerField(db_column='FndsAndOthrAccntsHldCnt', blank=True, null=True)  # Field name made lowercase.
    dnradvsdfndscntramt = models.BigIntegerField(db_column='DnrAdvsdFndsCntrAmt', blank=True, null=True)  # Field name made lowercase.
    fndsandothraccntscntramt = models.BigIntegerField(db_column='FndsAndOthrAccntsCntrAmt', blank=True, null=True)  # Field name made lowercase.
    dnradvsdfndsgrntsamt = models.BigIntegerField(db_column='DnrAdvsdFndsGrntsAmt', blank=True, null=True)  # Field name made lowercase.
    fndsandothraccntsgrntsamt = models.BigIntegerField(db_column='FndsAndOthrAccntsGrntsAmt', blank=True, null=True)  # Field name made lowercase.
    dnradvsdfndsvleoyamt = models.BigIntegerField(db_column='DnrAdvsdFndsVlEOYAmt', blank=True, null=True)  # Field name made lowercase.
    fndsandothraccntsvleoyamt = models.BigIntegerField(db_column='FndsAndOthrAccntsVlEOYAmt', blank=True, null=True)  # Field name made lowercase.
    dsclsdorglgctrlind = models.CharField(db_column='DsclsdOrgLgCtrlInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dsclsdfrchrtblprpsind = models.CharField(db_column='DsclsdFrChrtblPrpsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_i'


class ReturnSkeddPartIi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    prsrvtnpblcusind = models.CharField(db_column='PrsrvtnPblcUsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prtctnntrlhbttind = models.CharField(db_column='PrtctnNtrlHbttInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prsrvtnopnspcind = models.CharField(db_column='PrsrvtnOpnSpcInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hstrclndarind = models.CharField(db_column='HstrcLndArInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hstrcstrctrind = models.CharField(db_column='HstrcStrctrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ttlesmntscnt = models.BigIntegerField(db_column='TtlEsmntsCnt', blank=True, null=True)  # Field name made lowercase.
    ttlacrgcnt = models.DecimalField(db_column='TtlAcrgCnt', max_digits=22, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    hstrcstrctresmntscnt = models.BigIntegerField(db_column='HstrcStrctrEsmntsCnt', blank=True, null=True)  # Field name made lowercase.
    hstrcstrctresmntsaftrcnt = models.BigIntegerField(db_column='HstrcStrctrEsmntsAftrCnt', blank=True, null=True)  # Field name made lowercase.
    mdfdesmntscnt = models.BigIntegerField(db_column='MdfdEsmntsCnt', blank=True, null=True)  # Field name made lowercase.
    sttsesmntshldcnt = models.BigIntegerField(db_column='SttsEsmntsHldCnt', blank=True, null=True)  # Field name made lowercase.
    wrttnplcymntrngind = models.CharField(db_column='WrttnPlcyMntrngInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    stffhrsspntenfrcmntcnt = models.DecimalField(db_column='StffHrsSpntEnfrcmntCnt', max_digits=22, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    expnssincrrdenfrcmntamt = models.BigIntegerField(db_column='ExpnssIncrrdEnfrcmntAmt', blank=True, null=True)  # Field name made lowercase.
    sctn170hrqrstsfdind = models.CharField(db_column='Sctn170hRqrStsfdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_ii'


class ReturnSkeddPartIii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    artpblcexhbtnamnts_rvnsinclddamt = models.BigIntegerField(db_column='ArtPblcExhbtnAmnts_RvnsInclddAmt', blank=True, null=True)  # Field name made lowercase.
    artpblcexhbtnamnts_asstsinclddamt = models.BigIntegerField(db_column='ArtPblcExhbtnAmnts_AsstsInclddAmt', blank=True, null=True)  # Field name made lowercase.
    hldwrksart_rvnsinclddamt = models.BigIntegerField(db_column='HldWrksArt_RvnsInclddAmt', blank=True, null=True)  # Field name made lowercase.
    hldwrksart_asstsinclddamt = models.BigIntegerField(db_column='HldWrksArt_AsstsInclddAmt', blank=True, null=True)  # Field name made lowercase.
    skdd_cllctnusdpbexhbtnind = models.CharField(db_column='SkdD_CllctnUsdPbExhbtnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdd_cllusdschlrlyrsrchind = models.CharField(db_column='SkdD_CllUsdSchlrlyRsrchInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdd_cllctnusdprsrvtnind = models.CharField(db_column='SkdD_CllctnUsdPrsrvtnInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdd_cllusdlnorexchprgind = models.CharField(db_column='SkdD_CllUsdLnOrExchPrgInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdd_cllctnusdothrprpss = models.TextField(db_column='SkdD_CllctnUsdOthrPrpss', blank=True, null=True)  # Field name made lowercase.
    cllctnusdothrprpss_cllctnusdothrprpssind = models.CharField(db_column='CllctnUsdOthrPrpss_CllctnUsdOthrPrpssInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cllctnusdothrprpss_othrprpssdsc = models.CharField(db_column='CllctnUsdOthrPrpss_OthrPrpssDsc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    skdd_slctdasstsslind = models.CharField(db_column='SkdD_SlctdAsstsSlInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_iii'


class ReturnSkeddPartIv(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    agnttrstetcind = models.CharField(db_column='AgntTrstEtcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    bgnnngblncamt = models.BigIntegerField(db_column='BgnnngBlncAmt', blank=True, null=True)  # Field name made lowercase.
    addtnsdrngyramt = models.BigIntegerField(db_column='AddtnsDrngYrAmt', blank=True, null=True)  # Field name made lowercase.
    dstrbtnsdrngyramt = models.BigIntegerField(db_column='DstrbtnsDrngYrAmt', blank=True, null=True)  # Field name made lowercase.
    endngblncamt = models.BigIntegerField(db_column='EndngBlncAmt', blank=True, null=True)  # Field name made lowercase.
    inclescrwcstdlacctlbind = models.CharField(db_column='InclEscrwCstdlAcctLbInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    explntnprvddind = models.CharField(db_column='ExplntnPrvddInd', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_iv'


class ReturnSkeddPartIx(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    ttlbkvlothrasstsamt = models.BigIntegerField(db_column='TtlBkVlOthrAsstsAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_ix'


class ReturnSkeddPartV(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    cyendwmtfnd_bgnnngyrblncamt = models.BigIntegerField(db_column='CYEndwmtFnd_BgnnngYrBlncAmt', blank=True, null=True)  # Field name made lowercase.
    cyendwmtfnd_cntrbtnsamt = models.BigIntegerField(db_column='CYEndwmtFnd_CntrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    cyendwmtfnd_invstmnternngsorlsssamt = models.BigIntegerField(db_column='CYEndwmtFnd_InvstmntErnngsOrLsssAmt', blank=True, null=True)  # Field name made lowercase.
    cyendwmtfnd_grntsorschlrshpsamt = models.BigIntegerField(db_column='CYEndwmtFnd_GrntsOrSchlrshpsAmt', blank=True, null=True)  # Field name made lowercase.
    cyendwmtfnd_othrexpndtrsamt = models.BigIntegerField(db_column='CYEndwmtFnd_OthrExpndtrsAmt', blank=True, null=True)  # Field name made lowercase.
    cyendwmtfnd_admnstrtvexpnssamt = models.BigIntegerField(db_column='CYEndwmtFnd_AdmnstrtvExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    cyendwmtfnd_endyrblncamt = models.BigIntegerField(db_column='CYEndwmtFnd_EndYrBlncAmt', blank=True, null=True)  # Field name made lowercase.
    cymns1yrendwmtfnd_bgnnngyrblncamt = models.BigIntegerField(db_column='CYMns1YrEndwmtFnd_BgnnngYrBlncAmt', blank=True, null=True)  # Field name made lowercase.
    cymns1yrendwmtfnd_cntrbtnsamt = models.BigIntegerField(db_column='CYMns1YrEndwmtFnd_CntrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns1yrendwmtfnd_invstmnternngsorlsssamt = models.BigIntegerField(db_column='CYMns1YrEndwmtFnd_InvstmntErnngsOrLsssAmt', blank=True, null=True)  # Field name made lowercase.
    cymns1yrendwmtfnd_grntsorschlrshpsamt = models.BigIntegerField(db_column='CYMns1YrEndwmtFnd_GrntsOrSchlrshpsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns1yrendwmtfnd_othrexpndtrsamt = models.BigIntegerField(db_column='CYMns1YrEndwmtFnd_OthrExpndtrsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns1yrendwmtfnd_admnstrtvexpnssamt = models.BigIntegerField(db_column='CYMns1YrEndwmtFnd_AdmnstrtvExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    cymns1yrendwmtfnd_endyrblncamt = models.BigIntegerField(db_column='CYMns1YrEndwmtFnd_EndYrBlncAmt', blank=True, null=True)  # Field name made lowercase.
    cymns2yrendwmtfnd_bgnnngyrblncamt = models.BigIntegerField(db_column='CYMns2YrEndwmtFnd_BgnnngYrBlncAmt', blank=True, null=True)  # Field name made lowercase.
    cymns2yrendwmtfnd_cntrbtnsamt = models.BigIntegerField(db_column='CYMns2YrEndwmtFnd_CntrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns2yrendwmtfnd_invstmnternngsorlsssamt = models.BigIntegerField(db_column='CYMns2YrEndwmtFnd_InvstmntErnngsOrLsssAmt', blank=True, null=True)  # Field name made lowercase.
    cymns2yrendwmtfnd_grntsorschlrshpsamt = models.BigIntegerField(db_column='CYMns2YrEndwmtFnd_GrntsOrSchlrshpsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns2yrendwmtfnd_othrexpndtrsamt = models.BigIntegerField(db_column='CYMns2YrEndwmtFnd_OthrExpndtrsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns2yrendwmtfnd_admnstrtvexpnssamt = models.BigIntegerField(db_column='CYMns2YrEndwmtFnd_AdmnstrtvExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    cymns2yrendwmtfnd_endyrblncamt = models.BigIntegerField(db_column='CYMns2YrEndwmtFnd_EndYrBlncAmt', blank=True, null=True)  # Field name made lowercase.
    cymns3yrendwmtfnd_bgnnngyrblncamt = models.BigIntegerField(db_column='CYMns3YrEndwmtFnd_BgnnngYrBlncAmt', blank=True, null=True)  # Field name made lowercase.
    cymns3yrendwmtfnd_cntrbtnsamt = models.BigIntegerField(db_column='CYMns3YrEndwmtFnd_CntrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns3yrendwmtfnd_invstmnternngsorlsssamt = models.BigIntegerField(db_column='CYMns3YrEndwmtFnd_InvstmntErnngsOrLsssAmt', blank=True, null=True)  # Field name made lowercase.
    cymns3yrendwmtfnd_grntsorschlrshpsamt = models.BigIntegerField(db_column='CYMns3YrEndwmtFnd_GrntsOrSchlrshpsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns3yrendwmtfnd_othrexpndtrsamt = models.BigIntegerField(db_column='CYMns3YrEndwmtFnd_OthrExpndtrsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns3yrendwmtfnd_admnstrtvexpnssamt = models.BigIntegerField(db_column='CYMns3YrEndwmtFnd_AdmnstrtvExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    cymns3yrendwmtfnd_endyrblncamt = models.BigIntegerField(db_column='CYMns3YrEndwmtFnd_EndYrBlncAmt', blank=True, null=True)  # Field name made lowercase.
    cymns4yrendwmtfnd_bgnnngyrblncamt = models.BigIntegerField(db_column='CYMns4YrEndwmtFnd_BgnnngYrBlncAmt', blank=True, null=True)  # Field name made lowercase.
    cymns4yrendwmtfnd_cntrbtnsamt = models.BigIntegerField(db_column='CYMns4YrEndwmtFnd_CntrbtnsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns4yrendwmtfnd_invstmnternngsorlsssamt = models.BigIntegerField(db_column='CYMns4YrEndwmtFnd_InvstmntErnngsOrLsssAmt', blank=True, null=True)  # Field name made lowercase.
    cymns4yrendwmtfnd_grntsorschlrshpsamt = models.BigIntegerField(db_column='CYMns4YrEndwmtFnd_GrntsOrSchlrshpsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns4yrendwmtfnd_othrexpndtrsamt = models.BigIntegerField(db_column='CYMns4YrEndwmtFnd_OthrExpndtrsAmt', blank=True, null=True)  # Field name made lowercase.
    cymns4yrendwmtfnd_admnstrtvexpnssamt = models.BigIntegerField(db_column='CYMns4YrEndwmtFnd_AdmnstrtvExpnssAmt', blank=True, null=True)  # Field name made lowercase.
    cymns4yrendwmtfnd_endyrblncamt = models.BigIntegerField(db_column='CYMns4YrEndwmtFnd_EndYrBlncAmt', blank=True, null=True)  # Field name made lowercase.
    skdd_brddsgntdblnceoypct = models.DecimalField(db_column='SkdD_BrdDsgntdBlncEOYPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skdd_prmnntendwmntblnceoypct = models.DecimalField(db_column='SkdD_PrmnntEndwmntBlncEOYPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skdd_trmendwmntblnceoypct = models.DecimalField(db_column='SkdD_TrmEndwmntBlncEOYPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skdd_endwmntshldunrltdorgind = models.CharField(db_column='SkdD_EndwmntsHldUnrltdOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdd_endwmntshldrltdorgind = models.CharField(db_column='SkdD_EndwmntsHldRltdOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdd_rltdorglstschrind = models.CharField(db_column='SkdD_RltdOrgLstSchRInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_v'


class ReturnSkeddPartVi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    bldngs_dprctnamt = models.BigIntegerField(db_column='Bldngs_DprctnAmt', blank=True, null=True)  # Field name made lowercase.
    lshldimprvmnts_dprctnamt = models.BigIntegerField(db_column='LshldImprvmnts_DprctnAmt', blank=True, null=True)  # Field name made lowercase.
    eqpmnt_dprctnamt = models.BigIntegerField(db_column='Eqpmnt_DprctnAmt', blank=True, null=True)  # Field name made lowercase.
    othrlndbldngs_dprctnamt = models.BigIntegerField(db_column='OthrLndBldngs_DprctnAmt', blank=True, null=True)  # Field name made lowercase.
    skdd_ttlbkvllndbldngsamt = models.BigIntegerField(db_column='SkdD_TtlBkVlLndBldngsAmt', blank=True, null=True)  # Field name made lowercase.
    bldngs_invstmntcstorothrbssamt = models.BigIntegerField(db_column='Bldngs_InvstmntCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    eqpmnt_invstmntcstorothrbssamt = models.BigIntegerField(db_column='Eqpmnt_InvstmntCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    lnd_invstmntcstorothrbssamt = models.BigIntegerField(db_column='Lnd_InvstmntCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    lshldimprvmnts_invstmntcstorothrbssamt = models.BigIntegerField(db_column='LshldImprvmnts_InvstmntCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    othrlndbldngs_invstmntcstorothrbssamt = models.BigIntegerField(db_column='OthrLndBldngs_InvstmntCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    bldngs_othrcstorothrbssamt = models.BigIntegerField(db_column='Bldngs_OthrCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    eqpmnt_othrcstorothrbssamt = models.BigIntegerField(db_column='Eqpmnt_OthrCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    lnd_othrcstorothrbssamt = models.BigIntegerField(db_column='Lnd_OthrCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    lshldimprvmnts_othrcstorothrbssamt = models.BigIntegerField(db_column='LshldImprvmnts_OthrCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    othrlndbldngs_othrcstorothrbssamt = models.BigIntegerField(db_column='OthrLndBldngs_OthrCstOrOthrBssAmt', blank=True, null=True)  # Field name made lowercase.
    bldngs_bkvlamt = models.BigIntegerField(db_column='Bldngs_BkVlAmt', blank=True, null=True)  # Field name made lowercase.
    eqpmnt_bkvlamt = models.BigIntegerField(db_column='Eqpmnt_BkVlAmt', blank=True, null=True)  # Field name made lowercase.
    lnd_bkvlamt = models.BigIntegerField(db_column='Lnd_BkVlAmt', blank=True, null=True)  # Field name made lowercase.
    lshldimprvmnts_bkvlamt = models.BigIntegerField(db_column='LshldImprvmnts_BkVlAmt', blank=True, null=True)  # Field name made lowercase.
    othrlndbldngs_bkvlamt = models.BigIntegerField(db_column='OthrLndBldngs_BkVlAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_vi'


class ReturnSkeddPartVii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdd_ttlbkvlscrtsamt = models.BigIntegerField(db_column='SkdD_TtlBkVlScrtsAmt', blank=True, null=True)  # Field name made lowercase.
    clslyhldeqtyintrsts_bkvlamt = models.BigIntegerField(db_column='ClslyHldEqtyIntrsts_BkVlAmt', blank=True, null=True)  # Field name made lowercase.
    fnncldrvtvs_bkvlamt = models.BigIntegerField(db_column='FnnclDrvtvs_BkVlAmt', blank=True, null=True)  # Field name made lowercase.
    clslyhldeqtyintrsts_mthdvltncd = models.TextField(db_column='ClslyHldEqtyIntrsts_MthdVltnCd', blank=True, null=True)  # Field name made lowercase.
    fnncldrvtvs_mthdvltncd = models.TextField(db_column='FnnclDrvtvs_MthdVltnCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_vii'


class ReturnSkeddPartViii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    ttlbkvlprgrmrltdamt = models.BigIntegerField(db_column='TtlBkVlPrgrmRltdAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_viii'


class ReturnSkeddPartX(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    fdrlincmtxlbltyamt = models.BigIntegerField(db_column='FdrlIncmTxLbltyAmt', blank=True, null=True)  # Field name made lowercase.
    ttllbltyamt = models.BigIntegerField(db_column='TtlLbltyAmt', blank=True, null=True)  # Field name made lowercase.
    ftnttxtind = models.CharField(db_column='FtntTxtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_x'


class ReturnSkeddPartXi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    ttlrvetcadtdfnclstmtamt = models.BigIntegerField(db_column='TtlRvEtcAdtdFnclStmtAmt', blank=True, null=True)  # Field name made lowercase.
    ntunrlzdgnsinvstamt = models.BigIntegerField(db_column='NtUnrlzdGnsInvstAmt', blank=True, null=True)  # Field name made lowercase.
    dntdsrvcsandusfcltsamt = models.BigIntegerField(db_column='DntdSrvcsAndUsFcltsAmt', blank=True, null=True)  # Field name made lowercase.
    rcvrsprryrgrntsamt = models.BigIntegerField(db_column='RcvrsPrrYrGrntsAmt', blank=True, null=True)  # Field name made lowercase.
    othrrvnamt = models.BigIntegerField(db_column='OthrRvnAmt', blank=True, null=True)  # Field name made lowercase.
    rvnntrprtdamt = models.BigIntegerField(db_column='RvnNtRprtdAmt', blank=True, null=True)  # Field name made lowercase.
    rvnsbttlamt = models.BigIntegerField(db_column='RvnSbttlAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntexpnssntincldamt = models.BigIntegerField(db_column='InvstmntExpnssNtIncldAmt', blank=True, null=True)  # Field name made lowercase.
    othrrvnsntinclddamt = models.BigIntegerField(db_column='OthrRvnsNtInclddAmt', blank=True, null=True)  # Field name made lowercase.
    rvnntrprtdfnclstmtamt = models.BigIntegerField(db_column='RvnNtRprtdFnclStmtAmt', blank=True, null=True)  # Field name made lowercase.
    ttlrvnprfrm990amt = models.BigIntegerField(db_column='TtlRvnPrFrm990Amt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_xi'


class ReturnSkeddPartXii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    ttexpnsetcadtdfnclstmtamt = models.BigIntegerField(db_column='TtExpnsEtcAdtdFnclStmtAmt', blank=True, null=True)  # Field name made lowercase.
    dntdsrvcsusfcltsamt = models.BigIntegerField(db_column='DntdSrvcsUsFcltsAmt', blank=True, null=True)  # Field name made lowercase.
    prryradjstmntsamt = models.BigIntegerField(db_column='PrrYrAdjstmntsAmt', blank=True, null=True)  # Field name made lowercase.
    lsssrprtdamt = models.BigIntegerField(db_column='LsssRprtdAmt', blank=True, null=True)  # Field name made lowercase.
    othrexpnssinclddamt = models.BigIntegerField(db_column='OthrExpnssInclddAmt', blank=True, null=True)  # Field name made lowercase.
    expnssntrprtdamt = models.BigIntegerField(db_column='ExpnssNtRprtdAmt', blank=True, null=True)  # Field name made lowercase.
    expnsssbttlamt = models.BigIntegerField(db_column='ExpnssSbttlAmt', blank=True, null=True)  # Field name made lowercase.
    invstmntexpnssntincld2amt = models.BigIntegerField(db_column='InvstmntExpnssNtIncld2Amt', blank=True, null=True)  # Field name made lowercase.
    othrexpnssntinclddamt = models.BigIntegerField(db_column='OthrExpnssNtInclddAmt', blank=True, null=True)  # Field name made lowercase.
    expnssntrptfnclstmtamt = models.BigIntegerField(db_column='ExpnssNtRptFnclStmtAmt', blank=True, null=True)  # Field name made lowercase.
    ttlexpnssprfrm990amt = models.BigIntegerField(db_column='TtlExpnssPrFrm990Amt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedd_part_xii'


class ReturnSkedePartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    nndscrmntryplcystmtind = models.CharField(db_column='NndscrmntryPlcyStmtInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    plcystmtinbrchrsetcind = models.CharField(db_column='PlcyStmtInBrchrsEtcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    plcypblczdvbrdcstmdind = models.CharField(db_column='PlcyPblczdVBrdcstMdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mntnrclcmprcsind = models.CharField(db_column='MntnRclCmpRcsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mntnschlrshpsrcsind = models.CharField(db_column='MntnSchlrshpsRcsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mntncpyofbrchrsetcind = models.CharField(db_column='MntnCpyOfBrchrsEtcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mntncpyofallslind = models.CharField(db_column='MntnCpyOfAllSlInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dscrmntrcstdntsrghtsind = models.CharField(db_column='DscrmntRcStdntsRghtsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dscrmntrcadmssplcyind = models.CharField(db_column='DscrmntRcAdmssPlcyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dscrmntrcemplmfcltyind = models.CharField(db_column='DscrmntRcEmplmFcltyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dscrmntrcschsind = models.CharField(db_column='DscrmntRcSchsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dscrmntrcedcplcyind = models.CharField(db_column='DscrmntRcEdcPlcyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dscrmntrcusoffcltsind = models.CharField(db_column='DscrmntRcUsOfFcltsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dscrmntrcathltprgind = models.CharField(db_column='DscrmntRcAthltPrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dscrmntrcothractyind = models.CharField(db_column='DscrmntRcOthrActyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    gvrnmntfnncladrcvdind = models.CharField(db_column='GvrnmntFnnclAdRcvdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    gvrnmntfnncladrvkdind = models.CharField(db_column='GvrnmntFnnclAdRvkdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cmplncwthrvprc7550ind = models.CharField(db_column='CmplncWthRvPrc7550Ind', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skede_part_i'


class ReturnSkedfPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    grntrcrdsmntndind = models.CharField(db_column='GrntRcrdsMntndInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sbttloffcscnt = models.BigIntegerField(db_column='SbttlOffcsCnt', blank=True, null=True)  # Field name made lowercase.
    sbttlemplyscnt = models.BigIntegerField(db_column='SbttlEmplysCnt', blank=True, null=True)  # Field name made lowercase.
    cntnttnttloffccnt = models.BigIntegerField(db_column='CntnttnTtlOffcCnt', blank=True, null=True)  # Field name made lowercase.
    cntnttnttlemplycnt = models.BigIntegerField(db_column='CntnttnTtlEmplyCnt', blank=True, null=True)  # Field name made lowercase.
    ttloffccnt = models.BigIntegerField(db_column='TtlOffcCnt', blank=True, null=True)  # Field name made lowercase.
    ttlemplycnt = models.BigIntegerField(db_column='TtlEmplyCnt', blank=True, null=True)  # Field name made lowercase.
    sbttlspntamt = models.BigIntegerField(db_column='SbttlSpntAmt', blank=True, null=True)  # Field name made lowercase.
    cntntnspntamt = models.BigIntegerField(db_column='CntntnSpntAmt', blank=True, null=True)  # Field name made lowercase.
    ttlspntamt = models.BigIntegerField(db_column='TtlSpntAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedf_part_i'


class ReturnSkedfPartIi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    ttl501c3orgcnt = models.BigIntegerField(db_column='Ttl501c3OrgCnt', blank=True, null=True)  # Field name made lowercase.
    ttlothrorgcnt = models.BigIntegerField(db_column='TtlOthrOrgCnt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedf_part_ii'


class ReturnSkedfPartIv(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    trnsfrtfrgncrpind = models.CharField(db_column='TrnsfrTFrgnCrpInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    intrstinfrgntrstind = models.CharField(db_column='IntrstInFrgnTrstInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frgncrpownrshpind = models.CharField(db_column='FrgnCrpOwnrshpInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pssvfrgninvstmstcind = models.CharField(db_column='PssvFrgnInvstmstCInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    frgnprtnrshpind = models.CharField(db_column='FrgnPrtnrshpInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    bycttcntrsind = models.CharField(db_column='BycttCntrsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedf_part_iv'


class ReturnSkedgPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    mlslcttnsind = models.CharField(db_column='MlSlcttnsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emlslcttnsind = models.CharField(db_column='EmlSlcttnsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    phnslcttnsind = models.CharField(db_column='PhnSlcttnsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    inprsnslcttnsind = models.CharField(db_column='InPrsnSlcttnsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    slcttnofnngvtgrntsind = models.CharField(db_column='SlcttnOfNnGvtGrntsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    slcttnofgvtgrntsind = models.CharField(db_column='SlcttnOfGvtGrntsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    spclfndrsngevntsind = models.CharField(db_column='SpclFndrsngEvntsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    agrmtprffndrsngactyind = models.CharField(db_column='AgrmtPrfFndrsngActyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ttlgrssrcptsamt = models.BigIntegerField(db_column='TtlGrssRcptsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlrtndbycntrctrsamt = models.BigIntegerField(db_column='TtlRtndByCntrctrsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlnttorgnztnamt = models.BigIntegerField(db_column='TtlNtTOrgnztnAmt', blank=True, null=True)  # Field name made lowercase.
    allsttscd = models.TextField(db_column='AllSttsCd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedg_part_i'


class ReturnSkedgPartIi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    evnt1nm = models.CharField(db_column='Evnt1Nm', max_length=100, blank=True, null=True)  # Field name made lowercase.
    grssrcptsevnt1amt = models.BigIntegerField(db_column='GrssRcptsEvnt1Amt', blank=True, null=True)  # Field name made lowercase.
    chrtblcntrevnt1amt = models.BigIntegerField(db_column='ChrtblCntrEvnt1Amt', blank=True, null=True)  # Field name made lowercase.
    grssrvnevnt1amt = models.BigIntegerField(db_column='GrssRvnEvnt1Amt', blank=True, null=True)  # Field name made lowercase.
    cshprzsevnt1amt = models.BigIntegerField(db_column='CshPrzsEvnt1Amt', blank=True, null=True)  # Field name made lowercase.
    nncshprzsevnt1amt = models.BigIntegerField(db_column='NnCshPrzsEvnt1Amt', blank=True, null=True)  # Field name made lowercase.
    rntfcltycstsevnt1amt = models.BigIntegerField(db_column='RntFcltyCstsEvnt1Amt', blank=True, null=True)  # Field name made lowercase.
    fdandbvrgevnt1amt = models.BigIntegerField(db_column='FdAndBvrgEvnt1Amt', blank=True, null=True)  # Field name made lowercase.
    entrtnmntevnt1amt = models.BigIntegerField(db_column='EntrtnmntEvnt1Amt', blank=True, null=True)  # Field name made lowercase.
    othrdrctexpnssevnt1amt = models.BigIntegerField(db_column='OthrDrctExpnssEvnt1Amt', blank=True, null=True)  # Field name made lowercase.
    evnt2nm = models.CharField(db_column='Evnt2Nm', max_length=100, blank=True, null=True)  # Field name made lowercase.
    grssrcptsevnt2amt = models.BigIntegerField(db_column='GrssRcptsEvnt2Amt', blank=True, null=True)  # Field name made lowercase.
    chrtblcntrevnt2amt = models.BigIntegerField(db_column='ChrtblCntrEvnt2Amt', blank=True, null=True)  # Field name made lowercase.
    grssrvnevnt2amt = models.BigIntegerField(db_column='GrssRvnEvnt2Amt', blank=True, null=True)  # Field name made lowercase.
    cshprzsevnt2amt = models.BigIntegerField(db_column='CshPrzsEvnt2Amt', blank=True, null=True)  # Field name made lowercase.
    nncshprzsevnt2amt = models.BigIntegerField(db_column='NnCshPrzsEvnt2Amt', blank=True, null=True)  # Field name made lowercase.
    rntfcltycstsevnt2amt = models.BigIntegerField(db_column='RntFcltyCstsEvnt2Amt', blank=True, null=True)  # Field name made lowercase.
    fdandbvrgevnt2amt = models.BigIntegerField(db_column='FdAndBvrgEvnt2Amt', blank=True, null=True)  # Field name made lowercase.
    entrtnmntevnt2amt = models.BigIntegerField(db_column='EntrtnmntEvnt2Amt', blank=True, null=True)  # Field name made lowercase.
    othrdrctexpnssevnt2amt = models.BigIntegerField(db_column='OthrDrctExpnssEvnt2Amt', blank=True, null=True)  # Field name made lowercase.
    othrevntsttlcnt = models.BigIntegerField(db_column='OthrEvntsTtlCnt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsothrevntsamt = models.BigIntegerField(db_column='GrssRcptsOthrEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    chrtblcntrothrevntsamt = models.BigIntegerField(db_column='ChrtblCntrOthrEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    grssrvnothrevntsamt = models.BigIntegerField(db_column='GrssRvnOthrEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    cshprzsothrevntsamt = models.BigIntegerField(db_column='CshPrzsOthrEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    nncshprzsothrevntsamt = models.BigIntegerField(db_column='NnCshPrzsOthrEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    rntfcltycstsothrevntsamt = models.BigIntegerField(db_column='RntFcltyCstsOthrEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    fdandbvrgothrevntsamt = models.BigIntegerField(db_column='FdAndBvrgOthrEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    entrtnmntothrevntsamt = models.BigIntegerField(db_column='EntrtnmntOthrEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    othdrctexpnssothrevntsamt = models.BigIntegerField(db_column='OthDrctExpnssOthrEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    grssrcptsttlamt = models.BigIntegerField(db_column='GrssRcptsTtlAmt', blank=True, null=True)  # Field name made lowercase.
    chrtblcntrbtnsttamt = models.BigIntegerField(db_column='ChrtblCntrbtnsTtAmt', blank=True, null=True)  # Field name made lowercase.
    grssrvnttlevntsamt = models.BigIntegerField(db_column='GrssRvnTtlEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    cshprzsttlevntsamt = models.BigIntegerField(db_column='CshPrzsTtlEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    nncshprzsttlevntsamt = models.BigIntegerField(db_column='NnCshPrzsTtlEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    rntfcltycststtlevntsamt = models.BigIntegerField(db_column='RntFcltyCstsTtlEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    fdandbvrgttlevntsamt = models.BigIntegerField(db_column='FdAndBvrgTtlEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    entrtnmntttlevntsamt = models.BigIntegerField(db_column='EntrtnmntTtlEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    othdrctexpnssttlevntsamt = models.BigIntegerField(db_column='OthDrctExpnssTtlEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    drctexpnssmmryevntsamt = models.BigIntegerField(db_column='DrctExpnsSmmryEvntsAmt', blank=True, null=True)  # Field name made lowercase.
    ntincmsmmryamt = models.BigIntegerField(db_column='NtIncmSmmryAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedg_part_ii'


class ReturnSkedgPartIii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    gmnginfrmtn_grssrvnbngamt = models.BigIntegerField(db_column='GmngInfrmtn_GrssRvnBngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_cshprzsbngamt = models.BigIntegerField(db_column='GmngInfrmtn_CshPrzsBngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_nncshprzsbngamt = models.BigIntegerField(db_column='GmngInfrmtn_NnCshPrzsBngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_rntfcltycstsbngamt = models.BigIntegerField(db_column='GmngInfrmtn_RntFcltyCstsBngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_othrdrctexpnssbngamt = models.BigIntegerField(db_column='GmngInfrmtn_OthrDrctExpnssBngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_vlntrlbrbngind = models.CharField(db_column='GmngInfrmtn_VlntrLbrBngInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_vlntrlbrbngpct = models.DecimalField(db_column='GmngInfrmtn_VlntrLbrBngPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_grssrvnplltbsamt = models.BigIntegerField(db_column='GmngInfrmtn_GrssRvnPllTbsAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_cshprzsplltbsamt = models.BigIntegerField(db_column='GmngInfrmtn_CshPrzsPllTbsAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_nncshprzsplltbsamt = models.BigIntegerField(db_column='GmngInfrmtn_NnCshPrzsPllTbsAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_rntfcltycstsplltbsamt = models.BigIntegerField(db_column='GmngInfrmtn_RntFcltyCstsPllTbsAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_othrdrctexpnssplltbsamt = models.BigIntegerField(db_column='GmngInfrmtn_OthrDrctExpnssPllTbsAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_vlntrlbrplltbsind = models.CharField(db_column='GmngInfrmtn_VlntrLbrPllTbsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_vlntrlbrplltbspct = models.DecimalField(db_column='GmngInfrmtn_VlntrLbrPllTbsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_grssrvnothrgmngamt = models.BigIntegerField(db_column='GmngInfrmtn_GrssRvnOthrGmngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_cshprzsothrgmngamt = models.BigIntegerField(db_column='GmngInfrmtn_CshPrzsOthrGmngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_nncshprzsothrgmngamt = models.BigIntegerField(db_column='GmngInfrmtn_NnCshPrzsOthrGmngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_rntfcltycstsothrgmngamt = models.BigIntegerField(db_column='GmngInfrmtn_RntFcltyCstsOthrGmngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_othdrctexpnssothrgmngamt = models.BigIntegerField(db_column='GmngInfrmtn_OthDrctExpnssOthrGmngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_vlntrlbrothrgmngind = models.CharField(db_column='GmngInfrmtn_VlntrLbrOthrGmngInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_vlntrlbrothrgmngpct = models.DecimalField(db_column='GmngInfrmtn_VlntrLbrOthrGmngPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_grssrvnttlgmngamt = models.BigIntegerField(db_column='GmngInfrmtn_GrssRvnTtlGmngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_cshprzsttlgmngamt = models.BigIntegerField(db_column='GmngInfrmtn_CshPrzsTtlGmngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_nncshprzsttlgmngamt = models.BigIntegerField(db_column='GmngInfrmtn_NnCshPrzsTtlGmngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_rntfcltycststtlgmngamt = models.BigIntegerField(db_column='GmngInfrmtn_RntFcltyCstsTtlGmngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_othdrctexpnssttlgmngamt = models.BigIntegerField(db_column='GmngInfrmtn_OthDrctExpnssTtlGmngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_drctexpnssmmrygmngamt = models.BigIntegerField(db_column='GmngInfrmtn_DrctExpnsSmmryGmngAmt', blank=True, null=True)  # Field name made lowercase.
    gmnginfrmtn_ntgmngincmsmmryamt = models.BigIntegerField(db_column='GmngInfrmtn_NtGmngIncmSmmryAmt', blank=True, null=True)  # Field name made lowercase.
    skdg_lcnsdind = models.CharField(db_column='SkdG_LcnsdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdg_explntnifntxt = models.TextField(db_column='SkdG_ExplntnIfNTxt', blank=True, null=True)  # Field name made lowercase.
    skdg_lcnssspnddetcind = models.CharField(db_column='SkdG_LcnsSspnddEtcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdg_explntnifystxt = models.TextField(db_column='SkdG_ExplntnIfYsTxt', blank=True, null=True)  # Field name made lowercase.
    skdg_gmngwthnnmmbrsind = models.CharField(db_column='SkdG_GmngWthNnmmbrsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdg_mmbrofothrenttyind = models.CharField(db_column='SkdG_MmbrOfOthrEnttyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdg_gmngownfcltypct = models.DecimalField(db_column='SkdG_GmngOwnFcltyPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skdg_gmngothrfcltypct = models.DecimalField(db_column='SkdG_GmngOthrFcltyPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skdg_cntrctwth3rdprtyfrgmrvind = models.CharField(db_column='SkdG_CntrctWth3rdPrtyFrGmRvInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdg_gmngrvnrcvdbyorgamt = models.BigIntegerField(db_column='SkdG_GmngRvnRcvdByOrgAmt', blank=True, null=True)  # Field name made lowercase.
    skdg_gmngrvnrtnby3prtyamt = models.BigIntegerField(db_column='SkdG_GmngRvnRtnBy3PrtyAmt', blank=True, null=True)  # Field name made lowercase.
    skdg_gmngmngrcmpnstnamt = models.BigIntegerField(db_column='SkdG_GmngMngrCmpnstnAmt', blank=True, null=True)  # Field name made lowercase.
    skdg_gmngmngrsrvcsprvtxt = models.TextField(db_column='SkdG_GmngMngrSrvcsPrvTxt', blank=True, null=True)  # Field name made lowercase.
    skdg_gmngmngrisdrctrofcrind = models.CharField(db_column='SkdG_GmngMngrIsDrctrOfcrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdg_gmngmngrisemplyind = models.CharField(db_column='SkdG_GmngMngrIsEmplyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdg_gmngmngrisindcntrctind = models.CharField(db_column='SkdG_GmngMngrIsIndCntrctInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdg_chrtbldstrbtnrqrind = models.CharField(db_column='SkdG_ChrtblDstrbtnRqrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdg_dstrbtdamt = models.BigIntegerField(db_column='SkdG_DstrbtdAmt', blank=True, null=True)  # Field name made lowercase.
    skdg_indvdlwthbksnm = models.CharField(db_column='SkdG_IndvdlWthBksNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksnm_bsnssnmln1txt = models.CharField(db_column='PrsnsWthBksNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksnm_bsnssnmln2txt = models.CharField(db_column='PrsnsWthBksNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksusaddrss_addrssln1txt = models.CharField(db_column='PrsnsWthBksUSAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksusaddrss_addrssln2txt = models.CharField(db_column='PrsnsWthBksUSAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksusaddrss_ctynm = models.CharField(db_column='PrsnsWthBksUSAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksusaddrss_sttabbrvtncd = models.CharField(db_column='PrsnsWthBksUSAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksusaddrss_zipcd = models.CharField(db_column='PrsnsWthBksUSAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksfrgnaddrss_addrssln1txt = models.CharField(db_column='PrsnsWthBksFrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksfrgnaddrss_addrssln2txt = models.CharField(db_column='PrsnsWthBksFrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksfrgnaddrss_ctynm = models.TextField(db_column='PrsnsWthBksFrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    prsnswthbksfrgnaddrss_prvncorsttnm = models.TextField(db_column='PrsnsWthBksFrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    prsnswthbksfrgnaddrss_cntrycd = models.CharField(db_column='PrsnsWthBksFrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    prsnswthbksfrgnaddrss_frgnpstlcd = models.TextField(db_column='PrsnsWthBksFrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    skdg_thrdprtyprsnnm = models.CharField(db_column='SkdG_ThrdPrtyPrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    thrdprtybsnssnm_bsnssnmln1txt = models.CharField(db_column='ThrdPrtyBsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    thrdprtybsnssnm_bsnssnmln2txt = models.CharField(db_column='ThrdPrtyBsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    thrdprtyusaddrss_addrssln1txt = models.CharField(db_column='ThrdPrtyUSAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    thrdprtyusaddrss_addrssln2txt = models.CharField(db_column='ThrdPrtyUSAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    thrdprtyusaddrss_ctynm = models.CharField(db_column='ThrdPrtyUSAddrss_CtyNm', max_length=22, blank=True, null=True)  # Field name made lowercase.
    thrdprtyusaddrss_sttabbrvtncd = models.CharField(db_column='ThrdPrtyUSAddrss_SttAbbrvtnCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    thrdprtyusaddrss_zipcd = models.CharField(db_column='ThrdPrtyUSAddrss_ZIPCd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    thrdprtyfrgnaddrss_addrssln1txt = models.CharField(db_column='ThrdPrtyFrgnAddrss_AddrssLn1Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    thrdprtyfrgnaddrss_addrssln2txt = models.CharField(db_column='ThrdPrtyFrgnAddrss_AddrssLn2Txt', max_length=35, blank=True, null=True)  # Field name made lowercase.
    thrdprtyfrgnaddrss_ctynm = models.TextField(db_column='ThrdPrtyFrgnAddrss_CtyNm', blank=True, null=True)  # Field name made lowercase.
    thrdprtyfrgnaddrss_prvncorsttnm = models.TextField(db_column='ThrdPrtyFrgnAddrss_PrvncOrSttNm', blank=True, null=True)  # Field name made lowercase.
    thrdprtyfrgnaddrss_cntrycd = models.CharField(db_column='ThrdPrtyFrgnAddrss_CntryCd', max_length=2, blank=True, null=True)  # Field name made lowercase.
    thrdprtyfrgnaddrss_frgnpstlcd = models.TextField(db_column='ThrdPrtyFrgnAddrss_FrgnPstlCd', blank=True, null=True)  # Field name made lowercase.
    skdg_gmngmngrprsnnm = models.CharField(db_column='SkdG_GmngMngrPrsnNm', max_length=35, blank=True, null=True)  # Field name made lowercase.
    gmngmngrbsnssnm_bsnssnmln1txt = models.CharField(db_column='GmngMngrBsnssNm_BsnssNmLn1Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.
    gmngmngrbsnssnm_bsnssnmln2txt = models.CharField(db_column='GmngMngrBsnssNm_BsnssNmLn2Txt', max_length=75, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedg_part_iii'


class ReturnSkedhPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdh_fnnclassstncplcyind = models.CharField(db_column='SkdH_FnnclAssstncPlcyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdh_wrttnplcyind = models.CharField(db_column='SkdH_WrttnPlcyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdh_fpgrfrncfrcrind = models.CharField(db_column='SkdH_FPGRfrncFrCrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdh_fpgrfrncdscntdcrind = models.CharField(db_column='SkdH_FPGRfrncDscntdCrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdh_frcrmdcllyindgntind = models.CharField(db_column='SkdH_FrCrMdcllyIndgntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdh_fnnclassstncbdgtind = models.CharField(db_column='SkdH_FnnclAssstncBdgtInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdh_expnssexcdbdgtind = models.CharField(db_column='SkdH_ExpnssExcdBdgtInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdh_unbltprvdcrind = models.CharField(db_column='SkdH_UnblTPrvdCrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdh_annlcmmntybnftrprtind = models.CharField(db_column='SkdH_AnnlCmmntyBnftRprtInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdh_rprtpblcllyavlblind = models.CharField(db_column='SkdH_RprtPblcllyAvlblInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fnnclassstncatcsttyp_actvtsorprgrmscnt = models.BigIntegerField(db_column='FnnclAssstncAtCstTyp_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    fnnclassstncatcsttyp_prsnssrvdcnt = models.BigIntegerField(db_column='FnnclAssstncAtCstTyp_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    fnnclassstncatcsttyp_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='FnnclAssstncAtCstTyp_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    fnnclassstncatcsttyp_drctoffsttngrvnamt = models.BigIntegerField(db_column='FnnclAssstncAtCstTyp_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    fnnclassstncatcsttyp_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='FnnclAssstncAtCstTyp_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    fnnclassstncatcsttyp_ttlexpnspct = models.DecimalField(db_column='FnnclAssstncAtCstTyp_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    unrmbrsdmdcd_actvtsorprgrmscnt = models.BigIntegerField(db_column='UnrmbrsdMdcd_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    unrmbrsdmdcd_prsnssrvdcnt = models.BigIntegerField(db_column='UnrmbrsdMdcd_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    unrmbrsdmdcd_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='UnrmbrsdMdcd_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    unrmbrsdmdcd_drctoffsttngrvnamt = models.BigIntegerField(db_column='UnrmbrsdMdcd_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    unrmbrsdmdcd_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='UnrmbrsdMdcd_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    unrmbrsdmdcd_ttlexpnspct = models.DecimalField(db_column='UnrmbrsdMdcd_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    unrmbrsdcsts_actvtsorprgrmscnt = models.BigIntegerField(db_column='UnrmbrsdCsts_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    unrmbrsdcsts_prsnssrvdcnt = models.BigIntegerField(db_column='UnrmbrsdCsts_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    unrmbrsdcsts_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='UnrmbrsdCsts_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    unrmbrsdcsts_drctoffsttngrvnamt = models.BigIntegerField(db_column='UnrmbrsdCsts_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    unrmbrsdcsts_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='UnrmbrsdCsts_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    unrmbrsdcsts_ttlexpnspct = models.DecimalField(db_column='UnrmbrsdCsts_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    ttlfnnclassstnctyp_actvtsorprgrmscnt = models.BigIntegerField(db_column='TtlFnnclAssstncTyp_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    ttlfnnclassstnctyp_prsnssrvdcnt = models.BigIntegerField(db_column='TtlFnnclAssstncTyp_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    ttlfnnclassstnctyp_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='TtlFnnclAssstncTyp_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlfnnclassstnctyp_drctoffsttngrvnamt = models.BigIntegerField(db_column='TtlFnnclAssstncTyp_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ttlfnnclassstnctyp_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='TtlFnnclAssstncTyp_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlfnnclassstnctyp_ttlexpnspct = models.DecimalField(db_column='TtlFnnclAssstncTyp_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    cmmntyhlthsrvcs_actvtsorprgrmscnt = models.BigIntegerField(db_column='CmmntyHlthSrvcs_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    cmmntyhlthsrvcs_prsnssrvdcnt = models.BigIntegerField(db_column='CmmntyHlthSrvcs_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    cmmntyhlthsrvcs_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='CmmntyHlthSrvcs_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    cmmntyhlthsrvcs_drctoffsttngrvnamt = models.BigIntegerField(db_column='CmmntyHlthSrvcs_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    cmmntyhlthsrvcs_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='CmmntyHlthSrvcs_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    cmmntyhlthsrvcs_ttlexpnspct = models.DecimalField(db_column='CmmntyHlthSrvcs_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    hlthprfssnsedctn_actvtsorprgrmscnt = models.BigIntegerField(db_column='HlthPrfssnsEdctn_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    hlthprfssnsedctn_prsnssrvdcnt = models.BigIntegerField(db_column='HlthPrfssnsEdctn_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    hlthprfssnsedctn_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='HlthPrfssnsEdctn_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    hlthprfssnsedctn_drctoffsttngrvnamt = models.BigIntegerField(db_column='HlthPrfssnsEdctn_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    hlthprfssnsedctn_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='HlthPrfssnsEdctn_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    hlthprfssnsedctn_ttlexpnspct = models.DecimalField(db_column='HlthPrfssnsEdctn_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    sbsdzdhlthsrvcs_actvtsorprgrmscnt = models.BigIntegerField(db_column='SbsdzdHlthSrvcs_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    sbsdzdhlthsrvcs_prsnssrvdcnt = models.BigIntegerField(db_column='SbsdzdHlthSrvcs_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    sbsdzdhlthsrvcs_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='SbsdzdHlthSrvcs_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    sbsdzdhlthsrvcs_drctoffsttngrvnamt = models.BigIntegerField(db_column='SbsdzdHlthSrvcs_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    sbsdzdhlthsrvcs_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='SbsdzdHlthSrvcs_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    sbsdzdhlthsrvcs_ttlexpnspct = models.DecimalField(db_column='SbsdzdHlthSrvcs_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    rsrch_actvtsorprgrmscnt = models.BigIntegerField(db_column='Rsrch_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    rsrch_prsnssrvdcnt = models.BigIntegerField(db_column='Rsrch_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    rsrch_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='Rsrch_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    rsrch_drctoffsttngrvnamt = models.BigIntegerField(db_column='Rsrch_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    rsrch_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='Rsrch_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    rsrch_ttlexpnspct = models.DecimalField(db_column='Rsrch_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    cshandinkndcntrbtns_actvtsorprgrmscnt = models.BigIntegerField(db_column='CshAndInKndCntrbtns_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    cshandinkndcntrbtns_prsnssrvdcnt = models.BigIntegerField(db_column='CshAndInKndCntrbtns_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    cshandinkndcntrbtns_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='CshAndInKndCntrbtns_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    cshandinkndcntrbtns_drctoffsttngrvnamt = models.BigIntegerField(db_column='CshAndInKndCntrbtns_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    cshandinkndcntrbtns_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='CshAndInKndCntrbtns_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    cshandinkndcntrbtns_ttlexpnspct = models.DecimalField(db_column='CshAndInKndCntrbtns_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    ttlothrbnfts_actvtsorprgrmscnt = models.BigIntegerField(db_column='TtlOthrBnfts_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    ttlothrbnfts_prsnssrvdcnt = models.BigIntegerField(db_column='TtlOthrBnfts_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    ttlothrbnfts_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='TtlOthrBnfts_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlothrbnfts_drctoffsttngrvnamt = models.BigIntegerField(db_column='TtlOthrBnfts_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ttlothrbnfts_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='TtlOthrBnfts_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlothrbnfts_ttlexpnspct = models.DecimalField(db_column='TtlOthrBnfts_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    ttlcmmntybnfts_actvtsorprgrmscnt = models.BigIntegerField(db_column='TtlCmmntyBnfts_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    ttlcmmntybnfts_prsnssrvdcnt = models.BigIntegerField(db_column='TtlCmmntyBnfts_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    ttlcmmntybnfts_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='TtlCmmntyBnfts_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlcmmntybnfts_drctoffsttngrvnamt = models.BigIntegerField(db_column='TtlCmmntyBnfts_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ttlcmmntybnfts_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='TtlCmmntyBnfts_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlcmmntybnfts_ttlexpnspct = models.DecimalField(db_column='TtlCmmntyBnfts_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    skdh_allhsptlsplcyind = models.CharField(db_column='SkdH_AllHsptlsPlcyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdh_msthsptlsplcyind = models.CharField(db_column='SkdH_MstHsptlsPlcyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdh_indvhsptltlrdplcyind = models.CharField(db_column='SkdH_IndvHsptlTlrdPlcyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdh_prcnt100ind = models.CharField(db_column='SkdH_Prcnt100Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdh_prcnt150ind = models.CharField(db_column='SkdH_Prcnt150Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdh_prcnt200ind = models.CharField(db_column='SkdH_Prcnt200Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdh_frcrothprcntg = models.TextField(db_column='SkdH_FrCrOthPrcntg', blank=True, null=True)  # Field name made lowercase.
    frcrothprcntg_othrind = models.CharField(db_column='FrCrOthPrcntg_OthrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    frcrothprcntg_frcrothrpct = models.DecimalField(db_column='FrCrOthPrcntg_FrCrOthrPct', max_digits=22, decimal_places=12, blank=True, null=True)  # Field name made lowercase.
    skdh_prcnt200dind = models.CharField(db_column='SkdH_Prcnt200DInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdh_prcnt250ind = models.CharField(db_column='SkdH_Prcnt250Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdh_prcnt300ind = models.CharField(db_column='SkdH_Prcnt300Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdh_prcnt350ind = models.CharField(db_column='SkdH_Prcnt350Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdh_prcnt400ind = models.CharField(db_column='SkdH_Prcnt400Ind', max_length=1, blank=True, null=True)  # Field name made lowercase.
    skdh_dscntdcrothprcntg = models.TextField(db_column='SkdH_DscntdCrOthPrcntg', blank=True, null=True)  # Field name made lowercase.
    dscntdcrothprcntg_othrind = models.CharField(db_column='DscntdCrOthPrcntg_OthrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dscntdcrothprcntg_dscntdcrothrpct = models.DecimalField(db_column='DscntdCrOthPrcntg_DscntdCrOthrPct', max_digits=22, decimal_places=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedh_part_i'


class ReturnSkedhPartIi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    physclimprvandhsng_actvtsorprgrmscnt = models.BigIntegerField(db_column='PhysclImprvAndHsng_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    physclimprvandhsng_prsnssrvdcnt = models.BigIntegerField(db_column='PhysclImprvAndHsng_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    physclimprvandhsng_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='PhysclImprvAndHsng_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    physclimprvandhsng_drctoffsttngrvnamt = models.BigIntegerField(db_column='PhysclImprvAndHsng_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    physclimprvandhsng_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='PhysclImprvAndHsng_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    physclimprvandhsng_ttlexpnspct = models.DecimalField(db_column='PhysclImprvAndHsng_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    ecnmcdvlpmnt_actvtsorprgrmscnt = models.BigIntegerField(db_column='EcnmcDvlpmnt_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    ecnmcdvlpmnt_prsnssrvdcnt = models.BigIntegerField(db_column='EcnmcDvlpmnt_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    ecnmcdvlpmnt_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='EcnmcDvlpmnt_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ecnmcdvlpmnt_drctoffsttngrvnamt = models.BigIntegerField(db_column='EcnmcDvlpmnt_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ecnmcdvlpmnt_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='EcnmcDvlpmnt_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ecnmcdvlpmnt_ttlexpnspct = models.DecimalField(db_column='EcnmcDvlpmnt_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    cmmntyspprt_actvtsorprgrmscnt = models.BigIntegerField(db_column='CmmntySpprt_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    cmmntyspprt_prsnssrvdcnt = models.BigIntegerField(db_column='CmmntySpprt_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    cmmntyspprt_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='CmmntySpprt_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    cmmntyspprt_drctoffsttngrvnamt = models.BigIntegerField(db_column='CmmntySpprt_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    cmmntyspprt_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='CmmntySpprt_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    cmmntyspprt_ttlexpnspct = models.DecimalField(db_column='CmmntySpprt_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    envrnmntlimprvmnts_actvtsorprgrmscnt = models.BigIntegerField(db_column='EnvrnmntlImprvmnts_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    envrnmntlimprvmnts_prsnssrvdcnt = models.BigIntegerField(db_column='EnvrnmntlImprvmnts_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    envrnmntlimprvmnts_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='EnvrnmntlImprvmnts_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    envrnmntlimprvmnts_drctoffsttngrvnamt = models.BigIntegerField(db_column='EnvrnmntlImprvmnts_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    envrnmntlimprvmnts_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='EnvrnmntlImprvmnts_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    envrnmntlimprvmnts_ttlexpnspct = models.DecimalField(db_column='EnvrnmntlImprvmnts_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    ldrshpdvlpmnt_actvtsorprgrmscnt = models.BigIntegerField(db_column='LdrshpDvlpmnt_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    ldrshpdvlpmnt_prsnssrvdcnt = models.BigIntegerField(db_column='LdrshpDvlpmnt_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    ldrshpdvlpmnt_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='LdrshpDvlpmnt_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ldrshpdvlpmnt_drctoffsttngrvnamt = models.BigIntegerField(db_column='LdrshpDvlpmnt_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ldrshpdvlpmnt_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='LdrshpDvlpmnt_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ldrshpdvlpmnt_ttlexpnspct = models.DecimalField(db_column='LdrshpDvlpmnt_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    cltnbldng_actvtsorprgrmscnt = models.BigIntegerField(db_column='CltnBldng_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    cltnbldng_prsnssrvdcnt = models.BigIntegerField(db_column='CltnBldng_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    cltnbldng_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='CltnBldng_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    cltnbldng_drctoffsttngrvnamt = models.BigIntegerField(db_column='CltnBldng_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    cltnbldng_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='CltnBldng_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    cltnbldng_ttlexpnspct = models.DecimalField(db_column='CltnBldng_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    hlthimprvmntadvccy_actvtsorprgrmscnt = models.BigIntegerField(db_column='HlthImprvmntAdvccy_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    hlthimprvmntadvccy_prsnssrvdcnt = models.BigIntegerField(db_column='HlthImprvmntAdvccy_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    hlthimprvmntadvccy_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='HlthImprvmntAdvccy_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    hlthimprvmntadvccy_drctoffsttngrvnamt = models.BigIntegerField(db_column='HlthImprvmntAdvccy_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    hlthimprvmntadvccy_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='HlthImprvmntAdvccy_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    hlthimprvmntadvccy_ttlexpnspct = models.DecimalField(db_column='HlthImprvmntAdvccy_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    wrkfrcdvlpmnt_actvtsorprgrmscnt = models.BigIntegerField(db_column='WrkfrcDvlpmnt_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    wrkfrcdvlpmnt_prsnssrvdcnt = models.BigIntegerField(db_column='WrkfrcDvlpmnt_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    wrkfrcdvlpmnt_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='WrkfrcDvlpmnt_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    wrkfrcdvlpmnt_drctoffsttngrvnamt = models.BigIntegerField(db_column='WrkfrcDvlpmnt_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    wrkfrcdvlpmnt_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='WrkfrcDvlpmnt_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    wrkfrcdvlpmnt_ttlexpnspct = models.DecimalField(db_column='WrkfrcDvlpmnt_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    othrcmmnttybldngacty_actvtsorprgrmscnt = models.BigIntegerField(db_column='OthrCmmnttyBldngActy_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    othrcmmnttybldngacty_prsnssrvdcnt = models.BigIntegerField(db_column='OthrCmmnttyBldngActy_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    othrcmmnttybldngacty_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='OthrCmmnttyBldngActy_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    othrcmmnttybldngacty_drctoffsttngrvnamt = models.BigIntegerField(db_column='OthrCmmnttyBldngActy_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    othrcmmnttybldngacty_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='OthrCmmnttyBldngActy_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    othrcmmnttybldngacty_ttlexpnspct = models.DecimalField(db_column='OthrCmmnttyBldngActy_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.
    ttlcmmnttybldngacty_actvtsorprgrmscnt = models.BigIntegerField(db_column='TtlCmmnttyBldngActy_ActvtsOrPrgrmsCnt', blank=True, null=True)  # Field name made lowercase.
    ttlcmmnttybldngacty_prsnssrvdcnt = models.BigIntegerField(db_column='TtlCmmnttyBldngActy_PrsnsSrvdCnt', blank=True, null=True)  # Field name made lowercase.
    ttlcmmnttybldngacty_ttlcmmntybnftexpnsamt = models.BigIntegerField(db_column='TtlCmmnttyBldngActy_TtlCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlcmmnttybldngacty_drctoffsttngrvnamt = models.BigIntegerField(db_column='TtlCmmnttyBldngActy_DrctOffsttngRvnAmt', blank=True, null=True)  # Field name made lowercase.
    ttlcmmnttybldngacty_ntcmmntybnftexpnsamt = models.BigIntegerField(db_column='TtlCmmnttyBldngActy_NtCmmntyBnftExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    ttlcmmnttybldngacty_ttlexpnspct = models.DecimalField(db_column='TtlCmmnttyBldngActy_TtlExpnsPct', max_digits=6, decimal_places=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedh_part_ii'


class ReturnSkedhPartIii(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    bddbtexpnsrprtdind = models.CharField(db_column='BdDbtExpnsRprtdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    bddbtexpnsamt = models.BigIntegerField(db_column='BdDbtExpnsAmt', blank=True, null=True)  # Field name made lowercase.
    bddbtexpnsattrbtblamt = models.BigIntegerField(db_column='BdDbtExpnsAttrbtblAmt', blank=True, null=True)  # Field name made lowercase.
    rmbrsdbymdcramt = models.BigIntegerField(db_column='RmbrsdByMdcrAmt', blank=True, null=True)  # Field name made lowercase.
    cstofcrrmbrsdbymdcramt = models.BigIntegerField(db_column='CstOfCrRmbrsdByMdcrAmt', blank=True, null=True)  # Field name made lowercase.
    mdcrsrplsorshrtfllamt = models.BigIntegerField(db_column='MdcrSrplsOrShrtfllAmt', blank=True, null=True)  # Field name made lowercase.
    cstngmthdlgyusd = models.TextField(db_column='CstngMthdlgyUsd', blank=True, null=True)  # Field name made lowercase.
    cstaccntngsystmind = models.CharField(db_column='CstAccntngSystmInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    csttchrgrtind = models.CharField(db_column='CstTChrgRtInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    othrind = models.CharField(db_column='OthrInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wrttndbtcllctnplcyind = models.CharField(db_column='WrttnDbtCllctnPlcyInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fnnclassstncprvsnind = models.CharField(db_column='FnnclAssstncPrvsnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedh_part_iii'


class ReturnSkedhPartVa(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    hsptlfcltscnt = models.IntegerField(db_column='HsptlFcltsCnt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedh_part_va'


class ReturnSkedhPartVd(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    fcltynm = models.IntegerField(db_column='FcltyNm', blank=True, null=True)  # Field name made lowercase.
    othhlthcrfcltsnthsptl = models.TextField(db_column='OthHlthCrFcltsNtHsptl', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedh_part_vd'


class ReturnSkediPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    grntrcrdsmntndind = models.CharField(db_column='GrntRcrdsMntndInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedi_part_i'


class ReturnSkediPartIi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    ttl501c3orgcnt = models.BigIntegerField(db_column='Ttl501c3OrgCnt', blank=True, null=True)  # Field name made lowercase.
    ttlothrorgcnt = models.BigIntegerField(db_column='TtlOthrOrgCnt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedi_part_ii'


class ReturnSkedjPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    frstclssorchrtrtrvlind = models.CharField(db_column='FrstClssOrChrtrTrvlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trvlfrcmpnnsind = models.CharField(db_column='TrvlFrCmpnnsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idmnfctngrssuppmtsind = models.CharField(db_column='IdmnfctnGrssUpPmtsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dscrtnryspndngacctind = models.CharField(db_column='DscrtnrySpndngAcctInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hsngallwncorrsdncind = models.CharField(db_column='HsngAllwncOrRsdncInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pymntsfrusofrsdncind = models.CharField(db_column='PymntsFrUsOfRsdncInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    clbdsorfsind = models.CharField(db_column='ClbDsOrFsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prsnlsrvcsind = models.CharField(db_column='PrsnlSrvcsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wrttnplcyrftandeexpnssind = models.CharField(db_column='WrttnPlcyRfTAndEExpnssInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sbstnttnrqrdind = models.CharField(db_column='SbstnttnRqrdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cmpnstncmmttind = models.CharField(db_column='CmpnstnCmmttInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    indpndntcnsltntind = models.CharField(db_column='IndpndntCnsltntInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    frm990ofothrorgnztnsind = models.CharField(db_column='Frm990OfOthrOrgnztnsInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wrttnemplymntcntrctind = models.CharField(db_column='WrttnEmplymntCntrctInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cmpnstnsrvyind = models.CharField(db_column='CmpnstnSrvyInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    brdorcmmttapprvlind = models.CharField(db_column='BrdOrCmmttApprvlInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    svrncpymntind = models.CharField(db_column='SvrncPymntInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    spplmntlnnqlrtrplnind = models.CharField(db_column='SpplmntlNnqlRtrPlnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    eqtybsdcmparrngmind = models.CharField(db_column='EqtyBsdCmpArrngmInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cmpbsdonrvnofflngorgind = models.CharField(db_column='CmpBsdOnRvnOfFlngOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cmpbsdonrvrltdorgsind = models.CharField(db_column='CmpBsdOnRvRltdOrgsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cmpbsdnternsflngorgind = models.CharField(db_column='CmpBsdNtErnsFlngOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cmpbsdnternsrltdorgsind = models.CharField(db_column='CmpBsdNtErnsRltdOrgsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    anynnfxdpymntsind = models.CharField(db_column='AnyNnFxdPymntsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    intlcntrctexcptnind = models.CharField(db_column='IntlCntrctExcptnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rbttblprsmptnprcind = models.CharField(db_column='RbttblPrsmptnPrcInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedj_part_i'


class ReturnSkedlPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    tximpsdamt = models.BigIntegerField(db_column='TxImpsdAmt', blank=True, null=True)  # Field name made lowercase.
    txrmbrsdamt = models.BigIntegerField(db_column='TxRmbrsdAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedl_part_i'


class ReturnSkedlPartIi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    ttlblncdamt = models.BigIntegerField(db_column='TtlBlncDAmt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedl_part_ii'


class ReturnSkedmPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    skdm_frm8283rcvdcnt = models.BigIntegerField(db_column='SkdM_Frm8283RcvdCnt', blank=True, null=True)  # Field name made lowercase.
    skdm_anyprprtythtmstbhldind = models.CharField(db_column='SkdM_AnyPrprtyThtMstBHldInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdm_rvwprcssunslncgftsind = models.CharField(db_column='SkdM_RvwPrcssUnslNCGftsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    skdm_thrdprtsusdind = models.CharField(db_column='SkdM_ThrdPrtsUsdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    archlgclartfcts_nncshchckbxind = models.CharField(db_column='ArchlgclArtfcts_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    artfrctnlintrst_nncshchckbxind = models.CharField(db_column='ArtFrctnlIntrst_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    arthstrcltrsrs_nncshchckbxind = models.CharField(db_column='ArtHstrclTrsrs_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    btsandplns_nncshchckbxind = models.CharField(db_column='BtsAndPlns_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bksandpblctns_nncshchckbxind = models.CharField(db_column='BksAndPblctns_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crsandothrvhcls_nncshchckbxind = models.CharField(db_column='CrsAndOthrVhcls_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    clthngandhshldgds_nncshchckbxind = models.CharField(db_column='ClthngAndHshldGds_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cllctbls_nncshchckbxind = models.CharField(db_column='Cllctbls_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    drgsandmdclsppls_nncshchckbxind = models.CharField(db_column='DrgsAndMdclSppls_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fdinvntry_nncshchckbxind = models.CharField(db_column='FdInvntry_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hstrclartfcts_nncshchckbxind = models.CharField(db_column='HstrclArtfcts_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    intllctlprprty_nncshchckbxind = models.CharField(db_column='IntllctlPrprty_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qlfdcntrbhststrct_nncshchckbxind = models.CharField(db_column='QlfdCntrbHstStrct_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qlfdcntrbothr_nncshchckbxind = models.CharField(db_column='QlfdCntrbOthr_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rlesttcmmrcl_nncshchckbxind = models.CharField(db_column='RlEsttCmmrcl_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rlesttothr_nncshchckbxind = models.CharField(db_column='RlEsttOthr_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rlesttrsdntl_nncshchckbxind = models.CharField(db_column='RlEsttRsdntl_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scntfcspcmns_nncshchckbxind = models.CharField(db_column='ScntfcSpcmns_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scrprtnrshptrstintrsts_nncshchckbxind = models.CharField(db_column='ScrPrtnrshpTrstIntrsts_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scrtsclslyhldstck_nncshchckbxind = models.CharField(db_column='ScrtsClslyHldStck_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scrtsmsc_nncshchckbxind = models.CharField(db_column='ScrtsMsc_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scrtspblclytrdd_nncshchckbxind = models.CharField(db_column='ScrtsPblclyTrdd_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    txdrmy_nncshchckbxind = models.CharField(db_column='Txdrmy_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wrksofart_nncshchckbxind = models.CharField(db_column='WrksOfArt_NnCshChckbxInd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    archlgclartfcts_cntrbtncnt = models.BigIntegerField(db_column='ArchlgclArtfcts_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    artfrctnlintrst_cntrbtncnt = models.BigIntegerField(db_column='ArtFrctnlIntrst_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    arthstrcltrsrs_cntrbtncnt = models.BigIntegerField(db_column='ArtHstrclTrsrs_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    btsandplns_cntrbtncnt = models.BigIntegerField(db_column='BtsAndPlns_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    bksandpblctns_cntrbtncnt = models.BigIntegerField(db_column='BksAndPblctns_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    crsandothrvhcls_cntrbtncnt = models.BigIntegerField(db_column='CrsAndOthrVhcls_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    clthngandhshldgds_cntrbtncnt = models.BigIntegerField(db_column='ClthngAndHshldGds_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    cllctbls_cntrbtncnt = models.BigIntegerField(db_column='Cllctbls_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    drgsandmdclsppls_cntrbtncnt = models.BigIntegerField(db_column='DrgsAndMdclSppls_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    fdinvntry_cntrbtncnt = models.BigIntegerField(db_column='FdInvntry_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    hstrclartfcts_cntrbtncnt = models.BigIntegerField(db_column='HstrclArtfcts_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    intllctlprprty_cntrbtncnt = models.BigIntegerField(db_column='IntllctlPrprty_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    qlfdcntrbhststrct_cntrbtncnt = models.BigIntegerField(db_column='QlfdCntrbHstStrct_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    qlfdcntrbothr_cntrbtncnt = models.BigIntegerField(db_column='QlfdCntrbOthr_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    rlesttcmmrcl_cntrbtncnt = models.BigIntegerField(db_column='RlEsttCmmrcl_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    rlesttothr_cntrbtncnt = models.BigIntegerField(db_column='RlEsttOthr_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    rlesttrsdntl_cntrbtncnt = models.BigIntegerField(db_column='RlEsttRsdntl_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    scntfcspcmns_cntrbtncnt = models.BigIntegerField(db_column='ScntfcSpcmns_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    scrprtnrshptrstintrsts_cntrbtncnt = models.BigIntegerField(db_column='ScrPrtnrshpTrstIntrsts_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    scrtsclslyhldstck_cntrbtncnt = models.BigIntegerField(db_column='ScrtsClslyHldStck_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    scrtsmsc_cntrbtncnt = models.BigIntegerField(db_column='ScrtsMsc_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    scrtspblclytrdd_cntrbtncnt = models.BigIntegerField(db_column='ScrtsPblclyTrdd_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    txdrmy_cntrbtncnt = models.BigIntegerField(db_column='Txdrmy_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    wrksofart_cntrbtncnt = models.BigIntegerField(db_column='WrksOfArt_CntrbtnCnt', blank=True, null=True)  # Field name made lowercase.
    archlgclartfcts_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='ArchlgclArtfcts_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    artfrctnlintrst_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='ArtFrctnlIntrst_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    arthstrcltrsrs_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='ArtHstrclTrsrs_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    btsandplns_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='BtsAndPlns_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    bksandpblctns_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='BksAndPblctns_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    crsandothrvhcls_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='CrsAndOthrVhcls_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    clthngandhshldgds_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='ClthngAndHshldGds_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    cllctbls_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='Cllctbls_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    drgsandmdclsppls_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='DrgsAndMdclSppls_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    fdinvntry_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='FdInvntry_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    hstrclartfcts_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='HstrclArtfcts_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    intllctlprprty_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='IntllctlPrprty_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    qlfdcntrbhststrct_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='QlfdCntrbHstStrct_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    qlfdcntrbothr_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='QlfdCntrbOthr_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    rlesttcmmrcl_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='RlEsttCmmrcl_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    rlesttothr_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='RlEsttOthr_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    rlesttrsdntl_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='RlEsttRsdntl_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    scntfcspcmns_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='ScntfcSpcmns_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    scrprtnrshptrstintrsts_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='ScrPrtnrshpTrstIntrsts_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    scrtsclslyhldstck_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='ScrtsClslyHldStck_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    scrtsmsc_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='ScrtsMsc_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    scrtspblclytrdd_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='ScrtsPblclyTrdd_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    txdrmy_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='Txdrmy_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    wrksofart_nncshcntrbtnsrptf990amt = models.BigIntegerField(db_column='WrksOfArt_NncshCntrbtnsRptF990Amt', blank=True, null=True)  # Field name made lowercase.
    archlgclartfcts_mthdofdtrmnngrvnstxt = models.CharField(db_column='ArchlgclArtfcts_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    artfrctnlintrst_mthdofdtrmnngrvnstxt = models.CharField(db_column='ArtFrctnlIntrst_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    arthstrcltrsrs_mthdofdtrmnngrvnstxt = models.CharField(db_column='ArtHstrclTrsrs_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    btsandplns_mthdofdtrmnngrvnstxt = models.CharField(db_column='BtsAndPlns_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bksandpblctns_mthdofdtrmnngrvnstxt = models.CharField(db_column='BksAndPblctns_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    crsandothrvhcls_mthdofdtrmnngrvnstxt = models.CharField(db_column='CrsAndOthrVhcls_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    clthngandhshldgds_mthdofdtrmnngrvnstxt = models.CharField(db_column='ClthngAndHshldGds_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cllctbls_mthdofdtrmnngrvnstxt = models.CharField(db_column='Cllctbls_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    drgsandmdclsppls_mthdofdtrmnngrvnstxt = models.CharField(db_column='DrgsAndMdclSppls_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fdinvntry_mthdofdtrmnngrvnstxt = models.CharField(db_column='FdInvntry_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hstrclartfcts_mthdofdtrmnngrvnstxt = models.CharField(db_column='HstrclArtfcts_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    intllctlprprty_mthdofdtrmnngrvnstxt = models.CharField(db_column='IntllctlPrprty_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    qlfdcntrbhststrct_mthdofdtrmnngrvnstxt = models.CharField(db_column='QlfdCntrbHstStrct_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    qlfdcntrbothr_mthdofdtrmnngrvnstxt = models.CharField(db_column='QlfdCntrbOthr_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rlesttcmmrcl_mthdofdtrmnngrvnstxt = models.CharField(db_column='RlEsttCmmrcl_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rlesttothr_mthdofdtrmnngrvnstxt = models.CharField(db_column='RlEsttOthr_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rlesttrsdntl_mthdofdtrmnngrvnstxt = models.CharField(db_column='RlEsttRsdntl_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    scntfcspcmns_mthdofdtrmnngrvnstxt = models.CharField(db_column='ScntfcSpcmns_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    scrprtnrshptrstintrsts_mthdofdtrmnngrvnstxt = models.CharField(db_column='ScrPrtnrshpTrstIntrsts_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    scrtsclslyhldstck_mthdofdtrmnngrvnstxt = models.CharField(db_column='ScrtsClslyHldStck_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    scrtsmsc_mthdofdtrmnngrvnstxt = models.CharField(db_column='ScrtsMsc_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    scrtspblclytrdd_mthdofdtrmnngrvnstxt = models.CharField(db_column='ScrtsPblclyTrdd_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    txdrmy_mthdofdtrmnngrvnstxt = models.CharField(db_column='Txdrmy_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wrksofart_mthdofdtrmnngrvnstxt = models.CharField(db_column='WrksOfArt_MthdOfDtrmnngRvnsTxt', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedm_part_i'


class ReturnSkednPartI(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    lqdtnofasststbl = models.TextField(db_column='LqdtnOfAsstsTbl', blank=True, null=True)  # Field name made lowercase.
    drctrofsccssrind = models.CharField(db_column='DrctrOfSccssrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    emplyofsccssrind = models.CharField(db_column='EmplyOfSccssrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ownrofsccssrind = models.CharField(db_column='OwnrOfSccssrInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rcvcmpnstnind = models.CharField(db_column='RcvCmpnstnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    asstsdstrbtdind = models.CharField(db_column='AsstsDstrbtdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rqrdtntfyagind = models.CharField(db_column='RqrdTNtfyAGInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    attrnygnrlntfdind = models.CharField(db_column='AttrnyGnrlNtfdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lbltspdind = models.CharField(db_column='LbltsPdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    bndsotstndngind = models.CharField(db_column='BndsOtstndngInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    bndlbltsdschrgdind = models.CharField(db_column='BndLbltsDschrgdInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedn_part_i'


class ReturnSkednPartIi(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    drctrofsccssr2ind = models.CharField(db_column='DrctrOfSccssr2Ind', max_length=5, blank=True, null=True)  # Field name made lowercase.
    emplyofsccssr2ind = models.CharField(db_column='EmplyOfSccssr2Ind', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ownrofsccssr2ind = models.CharField(db_column='OwnrOfSccssr2Ind', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rcvcmpnstn2ind = models.CharField(db_column='RcvCmpnstn2Ind', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedn_part_ii'


class ReturnSkedrPartV(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    rcptofintanntsrntsryltsind = models.CharField(db_column='RcptOfIntAnntsRntsRyltsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    gftgrntorcpcntrtothorgind = models.CharField(db_column='GftGrntOrCpCntrTOthOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    gftgrntcpcntrfrmothorgind = models.CharField(db_column='GftGrntCpCntrFrmOthOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lnsorgrntstothrorgind = models.CharField(db_column='LnsOrGrntsTOthrOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lnsorgrntsfrmothorgind = models.CharField(db_column='LnsOrGrntsFrmOthOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dvrltdorgnztnind = models.CharField(db_column='DvRltdOrgnztnInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    asstsltothrorgind = models.CharField(db_column='AsstSlTOthrOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    asstprchsfrmothrorgind = models.CharField(db_column='AsstPrchsFrmOthrOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    asstexchngind = models.CharField(db_column='AsstExchngInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rntloffcltstothorgind = models.CharField(db_column='RntlOfFcltsTOthOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rntloffcltsfrmothorgind = models.CharField(db_column='RntlOfFcltsFrmOthOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prfrmofsrvcsfrothorgind = models.CharField(db_column='PrfrmOfSrvcsFrOthOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prfrmofsrvcsbyothrorgind = models.CharField(db_column='PrfrmOfSrvcsByOthrOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shrngoffcltsind = models.CharField(db_column='ShrngOfFcltsInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pdemplysshrngind = models.CharField(db_column='PdEmplysShrngInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rmbrsmntpdtothrorgind = models.CharField(db_column='RmbrsmntPdTOthrOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rmbrsmntpdbyothrorgind = models.CharField(db_column='RmbrsmntPdByOthrOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    trnsfrtothrorgind = models.CharField(db_column='TrnsfrTOthrOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.
    trnsfrfrmothrorgind = models.CharField(db_column='TrnsfrFrmOthrOrgInd', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_skedr_part_v'


class ReturnSpclcndtndsc(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    spclcndtndsc = models.TextField(db_column='SpclCndtnDsc', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_spclcndtndsc'


class ReturnSttswhrcpyofrtrnisfldcd(models.Model):
    object_id = models.CharField(max_length=31, blank=True, null=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    sttswhrcpyofrtrnisfldcd = models.CharField(db_column='SttsWhrCpyOfRtrnIsFldCd', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'return_sttswhrcpyofrtrnisfldcd'
