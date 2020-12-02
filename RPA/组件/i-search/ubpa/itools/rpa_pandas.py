# -*- coding: utf-8 -*-
'''
RPA 对pandas的一些封装
'''

def sort(df,values,ascending=False):
    '''
    sort(df,values)--> df

    功能:排序

    参数:
        df: pandas dateframe
        values   : 排序字段 "id,name"

    返回: 排序后的df

    例子: sort(["id","name"], ascending=False)
    '''
    values_list = values.split(",")
    return df.sort_values(values_list, ascending=ascending)

def group_sum(df,groupby,field=None):
    '''
    group_sum(df,groupby,field=None)--> df

    功能:分组统计 计算 合计

    参数:
        df: pandas dateframe
        groupby   : 排序字段 "id,name"
        field : 按照字段计算  "id,name"

    返回: 分组统计 计算合计后的df

    例子: group_sum(df,"id,name","id")
    '''
    return group_by(df, groupby, field, "sum")

def group_max(df,groupby,field=None):
    '''
        group_max(df,groupby,field=None)--> df

        功能:分组统计 过滤最大值

        参数:
            df: pandas dateframe
            groupby   : 排序字段 "id,name"
            field : 按照字段计算  "id,name"

        返回: 分组统计 过滤最大值的df

        例子: group_max(df,"id,name","id")
    '''
    return group_by(df, groupby, field, "max")

def group_min(df, groupby,field=None):
    '''
        group_min(df,groupby,field=None)--> df

        功能:分组统计 过滤最小值

        参数:
            df: pandas dateframe
            groupby   : 排序字段 "id,name"
            field : 按照字段计算  "id,name"

        返回: 分组统计 过滤最小值的df

        例子: group_min(df,"id,name","id")
    '''
    return group_by(df, groupby, field, "min")

def group_mean(df, groupby, field=None):
    '''
        group_mean(df,groupby,field=None)--> df

        功能:分组统计 计算平均数

        参数:
            df: pandas dateframe
            groupby   : 排序字段 "id,name"
            field : 按照字段计算  "id,name"

        返回: 分组统计 计算平均数的df

        例子: group_mean(df,"id,name","id")
    '''
    return group_by(df, groupby, field, "mean")

def rename(df,src_field,dst_field):
    '''
        rename(df,src_field,dst_field)

        功能:修改df列名

        参数:
            df: pandas dateframe
            src_field   : 原列名
            dst_field : 修改之后的列名

        返回: 无

        例子: rename(df,"id","newId")
    '''
    return df.rename(columns={src_field: dst_field})

def group_by(df,values,field,state):
    '''
    group_by(df,groupby,field=None)--> df

        功能:修改df列名

        参数:
            param df:  pandas dateframe
            param values: grouby字段
            param field: 按照字段计算
            param state: sum，max，min，mean

    :return: 统计过滤之后的df

    例子: group_by(df,"id,name","id,name","sum")
    '''
    values_list = values.split(",")
    if field != None:
        field_list = field.split(",")
        if state == "sum":
            return df.groupby(by=values_list, as_index=False)[field_list].sum()
        if state == "max":
            return df.groupby(by=values_list, as_index=False)[field_list].max()
        if state == "min":
            return df.groupby(by=values_list, as_index=False)[field_list].min()
        if state == "mean":
            return df.groupby(by=values_list, as_index=False)[field_list].mean()
    else:
        if state == "sum":
            return df.groupby(by=values_list, as_index=False).sum()
        if state == "max":
            return df.groupby(by=values_list, as_index=False).max()
        if state == "min":
            return df.groupby(by=values_list, as_index=False).min()
        if state == "mean":
            return df.groupby(by=values_list, as_index=False).mean()



