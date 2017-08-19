import graphene
from bradley.schema.types import User, Role, Contact, Pronouns, Tag
from bradley.schema.query import Query
from bradley.schema.mutation import Mutation


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[User, Role, Contact, Pronouns, Tag]
)
