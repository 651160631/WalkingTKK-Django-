#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Erick

import django_filters
from apps.users.models import UserProfile
from django.db.models import Q


class LoginErrorNumFilter(django_filters.rest_framework.FilterSet):
    """
    查询用户登录APP及登录教务系统错误次数的过滤类
    """

    tel = django_filters.CharFilter(tel='tel', lookup_expr='icontains')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(tel=value))

    class Meta:
        model = UserProfile
        fields = ['tel', ]
