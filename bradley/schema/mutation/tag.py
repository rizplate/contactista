import json
import graphene
from graphene import relay
from flask_security import current_user
from sqlalchemy.exc import IntegrityError
from bradley.models import db, Tag
from bradley.schema.types import UserError
from bradley.schema.types import Tag as TagType
from bradley.serializers import TagSerializer

class CreateTag(relay.ClientIDMutation):
    """
    Mutation to create a new tag
    """
    class Input:
        name = graphene.String(required=True)
        color = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    tag = graphene.Field(TagType)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if current_user.is_anonymous:
            return CreateTag(
                success=False,
                errors=[UserError(field="", message="Authentication required")]
            )

        serializer = TagSerializer(exclude=['user'])
        result = serializer.load(input)

        if result.errors:
            return CreateTag(
                success=False,
                errors=UserError.from_marshmallow(result.errors)
            )

        tag = result.data
        tag.user = current_user
        db.session.add(tag)

        try:
            db.session.commit()
        except IntegrityError:
            return CreateTag(
                success=False,
                errors=[UserError(
                    field="name",
                    message='Tag with name "{name}" already exists'.format(
                        name=tag.name
                    )
                )]
            )

        return CreateTag(
            success=True,
            tag=tag,
        )


class MutateTag(relay.ClientIDMutation):
    """
    Mutation to modify an existing tag
    """
    class Input:
        tag_id = graphene.Int(required=True)
        name = graphene.String()
        color = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    tag = graphene.Field(TagType)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if current_user.is_anonymous:
            return MutateTag(
                success=False,
                errors=[UserError(field="", message="Authentication required")]
            )

        tag_id = input['tag_id']
        tag = Tag.query.get(tag_id)
        if not tag or tag.user != current_user:
            return MutateTag(
                success=False,
                errors=[UserError(
                    field="tag_id",
                    message="Tag not found"
                )]
            )

        serializer = TagSerializer(exclude=['user'])
        result = serializer.load(input, instance=tag)

        if result.errors:
            return CreateTag(
                success=False,
                errors=UserError.from_marshmallow(result.errors)
            )

        db.session.add(result.data)
        db.session.commit()

        return MutateTag(
            success=True,
            tag=tag,
        )


class DestroyTag(relay.ClientIDMutation):
    """
    Mutation to delete an existing tag
    """
    class Input:
        tag_id = graphene.Int(required=True)

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    tag = graphene.Field(TagType)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if current_user.is_anonymous:
            return DestroyTag(
                success=False,
                errors=[UserError(field="", message="Authentication required")]
            )

        tag_id = input['tag_id']
        tag = Tag.query.get(tag_id)
        if not tag or contact.user != current_user:
            return DestroyTag(
                success=False,
                errors=[UserError(
                    field="tag_id",
                    message="Tag not found"
                )]
            )

        db.session.delete(tag)
        db.session.commit()

        return DestroyTag(
            success=True,
            tag=tag,
        )
