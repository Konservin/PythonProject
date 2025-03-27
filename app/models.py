from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base


class Filter(Base):
    __tablename__ = "filter"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

    # 👇 Add relationship
    criteria = relationship("Criteria", back_populates="filter", cascade="all, delete-orphan")

class Criteria(Base):
    __tablename__ = "criteria"
    id = Column(Integer, primary_key=True, index=True)
    filter_id = Column(Integer, ForeignKey("filter.id"))
    type_id = Column(Integer, ForeignKey("filter_types.id"))
    subtype_id = Column(Integer, ForeignKey("filter_subtypes.id"))
    value = Column(String(255))

    # 👇 Backref to Filter
    filter = relationship("Filter", back_populates="criteria")
    filter_type = relationship("FilterType", back_populates="criteria")
    filter_subtype = relationship("FilterSubtype", back_populates="criteria")


class FilterType(Base):
    __tablename__ = "filter_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

    # 👇 Backref to Filter
    criteria = relationship("Criteria", back_populates="filter_type")
    subtypes = relationship("FilterSubtype", back_populates="filter_type")
    subtype_assocs = relationship("TypeSubtypeAssoc", back_populates="type")

    @property
    def value_type(self):
        if self.value_type_info:
            return self.value_type_info[0].value_type
        return "string"

class FilterSubtype(Base):
    __tablename__ = "filter_subtypes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    type_id = Column(Integer, ForeignKey("filter_types.id"))

    # 👇 Backref to Filter
    filter_type = relationship("FilterType", back_populates="subtypes")
    criteria = relationship("Criteria", back_populates="filter_subtype")
    type_assocs = relationship("TypeSubtypeAssoc", back_populates="subtype")

class TypeSubtypeAssoc(Base):
    __tablename__ = "types_subtypes_assoc"
    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("filter_types.id"))
    subtype_id = Column(Integer, ForeignKey("filter_subtypes.id"))

    # Relationships
    type = relationship("FilterType", back_populates="subtype_assocs")
    subtype = relationship("FilterSubtype", back_populates="type_assocs")

class FilterValueType(Base):
    __tablename__ = "filter_values"
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey("filter_types.id"))
    value_type = Column(String(50))  # "int", "string", "date"

    type = relationship("FilterType", backref="value_type_info")

