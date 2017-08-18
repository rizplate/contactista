import json
import graphene
from graphene import relay
from flask_security import current_user
from bradley.models import db, Contact
from bradley.schema.types import UserError
from bradley.schema.types import Contact as ContactType
from bradley.serializers import ContactSerializer
from .input import PronounsInput, ContactNameInput, ContactEmailInput

class CreateContact(relay.ClientIDMutation):
    """
    Mutation to create a new contact
    """
    class Input:
        pronoun = graphene.String()
        pronouns = graphene.Field(PronounsInput)
        pronouns_list = graphene.List(PronounsInput)
        name = graphene.String()
        names = graphene.List(ContactNameInput)
        email = graphene.String()
        emails = graphene.List(ContactEmailInput)
        notes = graphene.String()
        notes_format = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    contact = graphene.Field(ContactType)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if current_user.is_anonymous:
            return CreateContact(
                success=False,
                errors=[UserError(field="", message="Authentication required")]
            )

        serializer = ContactSerializer(exclude=['user'])
        result = serializer.load(input)

        if result.errors:
            return CreateContact(
                success=False,
                errors=UserError.from_marshmallow(result.errors)
            )

        contact = result.data
        contact.user = current_user
        db.session.add(contact)
        db.session.commit()

        return CreateContact(
            success=True,
            contact=contact,
        )


class MutateContact(relay.ClientIDMutation):
    """
    Mutation to modify an existing contact
    """
    class Input:
        id = graphene.Int(required=True)
        pronoun = graphene.String()
        pronouns = graphene.Field(PronounsInput)
        pronouns_list = graphene.List(PronounsInput)
        name = graphene.String()
        names = graphene.List(ContactNameInput)
        email = graphene.String()
        emails = graphene.List(ContactEmailInput)
        notes = graphene.String()
        notes_format = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    contact = graphene.Field(ContactType)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if current_user.is_anonymous:
            return MutateContact(
                success=False,
                errors=[UserError(field="", message="Authentication required")]
            )

        contact_id = input.get('id')
        contact = Contact.query.get(contact_id)
        if not contact or contact.user != current_user:
            return MutateContact(
                success=False,
                errors=[UserError(
                    field="clientMutationId",
                    message="Contact not found"
                )]
            )

        serializer = ContactSerializer(exclude=['user'])
        result = serializer.load(input, instance=contact)

        if result.errors:
            return CreateContact(
                success=False,
                errors=UserError.from_marshmallow(result.errors)
            )

        db.session.add(result.data)
        db.session.commit()

        return MutateContact(
            success=True,
            contact=contact,
        )


class DestroyContact(relay.ClientIDMutation):
    """
    Mutation to delete an existing contact
    """
    class Input:
        id = graphene.Int(required=True)

    success = graphene.Boolean()
    errors = graphene.List(UserError)
    contact = graphene.Field(ContactType)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        if current_user.is_anonymous:
            return DestroyContact(
                success=False,
                errors=[UserError(field="", message="Authentication required")]
            )

        contact_id = input.get('id')
        contact = Contact.query.get(contact_id)
        if not contact or contact.user != current_user:
            return DestroyContact(
                success=False,
                errors=[UserError(
                    field="clientMutationId",
                    message="Contact not found"
                )]
            )

        db.session.delete(contact)
        db.session.commit()

        return DestroyContact(
            success=True,
            contact=contact,
        )
