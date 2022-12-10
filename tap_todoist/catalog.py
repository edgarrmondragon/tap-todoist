from singer_sdk._singerlib import Schema
from singer_sdk import typing as th


class PropertiesList(th.PropertiesList):
    def to_schema(self) -> Schema:
        """Return a Schema object for this property list."""
        return Schema.from_dict(self.to_dict())


SCHEMAS = {
    "projects": PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("color", th.StringType),
        th.Property("parent_id", th.StringType),
        th.Property("child_order", th.IntegerType),
        th.Property("collapsed", th.BooleanType),
        th.Property("shared", th.BooleanType),
        th.Property("is_deleted", th.BooleanType),
        th.Property("is_archived", th.BooleanType),
        th.Property("is_favorite", th.BooleanType),
        th.Property("inbox_project", th.BooleanType),
        th.Property("team_inbox", th.BooleanType),
        th.Property("view_style", th.StringType, allowed_values=["list", "board"]),
    ),
    "items": PropertiesList(
        th.Property("id", th.StringType),
        th.Property("user_id", th.StringType),
        th.Property("project_id", th.StringType),
        th.Property("content", th.StringType),
        th.Property("description", th.StringType),
        th.Property(
            "due",
            th.ObjectType(
                th.Property("date", th.StringType),
                th.Property("is_recurring", th.BooleanType),
                th.Property("string", th.StringType),
                th.Property("timezone", th.StringType),
                th.Property("lang", th.StringType),
            ),
        ),
        th.Property("priority", th.IntegerType),
        th.Property("parent_id", th.StringType),
        th.Property("child_order", th.IntegerType),
        th.Property("section_id", th.StringType),
        th.Property("day_order", th.IntegerType),
        th.Property("collapsed", th.IntegerType),
        th.Property("labels", th.ArrayType(th.StringType)),
        th.Property("added_by_uid", th.StringType),
        th.Property("assigned_by_uid", th.StringType),
        th.Property("responsible_uid", th.StringType),
        th.Property("checked", th.IntegerType),
        th.Property("is_deleted", th.BooleanType),
        th.Property("completed_at", th.StringType),
        th.Property("added_at", th.StringType),
    ),
    "sections": PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("project_id", th.StringType),
        th.Property("section_order", th.IntegerType),
        th.Property("collapsed", th.IntegerType),
        th.Property("is_deleted", th.BooleanType),
        th.Property("is_archived", th.BooleanType),
        th.Property("archived_at", th.StringType),
        th.Property("added_at", th.StringType),
    ),
    "labels": PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("color", th.StringType),
        th.Property("item_order", th.IntegerType),
        th.Property("is_deleted", th.BooleanType),
        th.Property("is_favorite", th.BooleanType),
    ),
    "notes": PropertiesList(
        th.Property(
            "id",
            th.StringType,
            required=True,
            description="The ID of the note.",
        ),
        th.Property(
            "posted_uid",
            th.StringType,
            description="The ID of the user that posted the note.",
        ),
        th.Property(
            "item_id",
            th.StringType,
            description="The item which the is part of.",
        ),
        th.Property(
            "content",
            th.StringType,
            description="The content of the note.",
        ),
        th.Property(
            "file_attachment",
            th.ObjectType(
                th.Property(
                    "file_name",
                    th.StringType,
                    description="The name of the file.",
                ),
                th.Property(
                    "file_size",
                    th.IntegerType,
                    description="The size of the file in bytes.",
                ),
                th.Property(
                    "file_type",
                    th.StringType,
                    description="MIME type (for example `text/plain` or `image/png`).",
                ),
                th.Property(
                    "file_url",
                    th.StringType,
                    description="The URL where the file is located.",
                ),
                th.Property(
                    "upload_state",
                    th.StringType,
                    description=(
                        "Upload completion state (for example `pending` or "
                        "`completed`)."
                    ),
                ),
            ),
            description="A file attached to the note.",
        ),
        th.Property(
            "is_deleted",
            th.BooleanType,
            description="Whether the note is marked as deleted.",
        ),
        th.Property(
            "posted_at",
            th.DateTimeType,
            description="The date and time when the note was posted.",
        ),
        th.Property(
            "reactions",
            th.ObjectType(
                additional_properties=th.ArrayType(th.ArrayType(th.StringType))
            ),
            description="List of emoji reactions and corresponding user IDs.",
        ),
    ),
    "filters": PropertiesList(
        th.Property(
            "id",
            th.StringType,
            required=True,
            description="The ID of the filter.",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The name of the filter.",
        ),
        th.Property(
            "query",
            th.StringType,
            description="The query to search for.",
        ),
        th.Property(
            "color",
            th.StringType,
            description="The color of the filter icon.",
            allowed_values=[
                "berry_red",
                "red",
                "orange",
                "yellow",
                "olive_green",
                "lime_green",
                "green",
                "mint_green",
                "teal",
                "sky_blue",
                "light_blue",
                "blue",
                "grape",
                "violet",
                "lavender",
                "magenta",
                "salmon",
                "charcoal",
                "grey",
                "taupe",
            ],
        ),
        th.Property(
            "item_order",
            th.IntegerType,
            description="Filter's order in the filter list.",
        ),
        th.Property(
            "is_deleted",
            th.BooleanType,
            description="Whether the filter is marked as deleted.",
        ),
        th.Property(
            "is_favorite",
            th.BooleanType,
            description="Whether the filter is a favorite.",
        ),
    ),
    "reminders": PropertiesList(
        th.Property(
            "id",
            th.StringType,
            required=True,
            description="The ID of the reminder.",
        ),
        th.Property(
            "notify_uid",
            th.StringType,
            description="The user ID which should be notified of the reminder.",
        ),
        th.Property(
            "item_id",
            th.StringType,
            description="The item ID which the reminder is about.",
        ),
        th.Property(
            "type",
            th.StringType,
            description="The type of the reminder.",
            allowed_values=["relative", "absolute", "location"],
        ),
        th.Property(
            "nm_offset",
            th.IntegerType,
            description=(
                "The relative time in minutes before the reminder before the due date "
                "of the item, in which the reminder should be triggered."
            ),
        ),
        th.Property(
            "loc_lat",
            th.StringType,
            description="The location latitude.",
        ),
        th.Property(
            "loc_long",
            th.StringType,
            description="The location longitude.",
        ),
        th.Property(
            "loc_trigger",
            th.StringType,
            description="What should trigger the reminder.",
            allowed_values=["on_enter", "on_leave"],
        ),
        th.Property(
            "radius",
            th.IntegerType,
            description=(
                "The radius of the location that is still considered to as part of the "
                "location."
            ),
        ),
        th.Property(
            "is_deleted",
            th.IntegerType,
            description="Whether the reminder is marked as deleted.",
        ),
    ),
}
