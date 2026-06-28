package com.zbw.domain;

import java.util.ArrayList;
import java.util.List;

public class AdminExample {
    protected String orderByClause;
    protected boolean distinct;
    protected List<Criteria> oredCriteria = new ArrayList<>();

    public void setOrderByClause(String orderByClause) { this.orderByClause = orderByClause; }
    public String getOrderByClause() { return orderByClause; }
    public void setDistinct(boolean distinct) { this.distinct = distinct; }
    public boolean isDistinct() { return distinct; }
    public List<Criteria> getOredCriteria() { return oredCriteria; }
    public Criteria createCriteria() {
        Criteria criteria = new Criteria();
        if (oredCriteria.isEmpty()) {
            oredCriteria.add(criteria);
        }
        return criteria;
    }
    public void clear() {
        oredCriteria.clear();
        orderByClause = null;
        distinct = false;
    }

    public static class Criteria {
        protected List<Criterion> criteria = new ArrayList<>();
        public boolean isValid() { return !criteria.isEmpty(); }
        public List<Criterion> getCriteria() { return criteria; }
        public Criteria andAdminNameEqualTo(String value) {
            criteria.add(new Criterion("admin_name =", value));
            return this;
        }
    }

    public static class Criterion {
        private final String condition;
        private final Object value;
        private final boolean noValue;
        private final boolean singleValue;
        private final boolean betweenValue = false;
        private final boolean listValue = false;
        private final Object secondValue = null;

        public Criterion(String condition, Object value) {
            this.condition = condition;
            this.value = value;
            this.noValue = false;
            this.singleValue = true;
        }
        public String getCondition() { return condition; }
        public Object getValue() { return value; }
        public Object getSecondValue() { return secondValue; }
        public boolean isNoValue() { return noValue; }
        public boolean isSingleValue() { return singleValue; }
        public boolean isBetweenValue() { return betweenValue; }
        public boolean isListValue() { return listValue; }
    }
}
