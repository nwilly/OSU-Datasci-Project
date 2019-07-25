import pandas

#load raw data
data = pandas.read_csv("classes_spring_raw.csv", low_memory=False)

#delete non-useful columns
data.drop(data.columns[30:], axis=1, inplace=True)
data.drop('DERIVED_SSTSNAV_PERSON_NAME', axis=1, inplace=True)
data.drop('DERIVED_REGFRM1_SS_TRANSACT_TITLE', axis=1, inplace=True)
data.drop('DERIVED_REGFRM1_TITLE1', axis=1, inplace=True)
data.drop('DERIVED_CLSRCH_SSS_PAGE_KEYDESCR', axis=1, inplace=True)
data.drop('SSR_CLS_DTL_WRK_SSR_DESCRSHORT', axis=1, inplace=True)
data.drop('PSXLATITEM_XLATLONGNAME$31$', axis=1, inplace=True)
data.drop('CAMPUS_LOC_VW_DESCR', axis=1, inplace=True)
data.drop('CAMPUS_TBL_DESCR', axis=1, inplace=True)
data.drop('SSR_CLS_DTL_WRK_SSR_CLS_TXB_MSG', axis=1, inplace=True)
data.drop('PSTEXT', axis=1, inplace=True)
data.drop('DERIVED_CLSRCH_SSR_CLASSNOTE_LONG', axis=1, inplace=True)
data.drop('SSR_CLS_DTL_WRK_SSR_DATE_LONG', axis=1, inplace=True)
data.drop('INSTRUCT_MODE_DESCR', axis=1, inplace=True)
data.drop('SSR_CLS_DTL_WRK_SSR_CRSE_ATTR_LONG', axis=1, inplace=True)


#rename columns
data.rename(index=str, columns={data.columns[0]: "CLASS_NAME",
                                data.columns[1]: "CLASS_ID",
                                data.columns[2]: "CLASS_CREDITS",
                                data.columns[3]: "STUDENT_TYPE",
                                data.columns[4]: "GRADE_BASIS",
                                data.columns[5]: "MTG_SCHED",
                                data.columns[6]: "MTG_LOC",
                                data.columns[7]: "INSTRUCTOR",
                                data.columns[8]: "MTG_DATE",
                                data.columns[9]: "PREREQUISITES",
                                data.columns[10]: "ENROLL_CAP",
                                data.columns[11]: "WAIT_CAP",
                                data.columns[12]: "ENROLL_NUM",
                                data.columns[13]: "WAIT_NUM",
                                data.columns[14]: "AVAILABLE_SEATS",
                                data.columns[15]: "CLASS_DESCRIPTION"},
            inplace=True)

data.to_csv("Classes_spring_cleaned.csv")
