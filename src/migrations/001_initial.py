"""Peewee migrations -- 001_initial.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    
    @migrator.create_model
    class Coin(pw.Model):
        coin_id = pw.UUIDField(primary_key=True)
        coin_name = pw.CharField(max_length=255, unique=True)
        is_complete = pw.BooleanField(default=False)

        class Meta:
            table_name = "coin"
            schema = "coins"

    @migrator.create_model
    class Duty(pw.Model):
        duty_id = pw.UUIDField(primary_key=True)
        duty_name = pw.CharField(max_length=255, unique=True)
        duty_desc = pw.CharField(max_length=255)

        class Meta:
            table_name = "duty"
            schema = "coins"

    @migrator.create_model
    class Junction(pw.Model):
        junction_id = pw.UUIDField(primary_key=True)
        duty_id = pw.ForeignKeyField(column_name='duty_id', field='duty_id', model=migrator.orm['duty'], on_delete='CASCADE', on_update='CASCADE')
        coin_id = pw.ForeignKeyField(column_name='coin_id', field='coin_id', model=migrator.orm['coin'], on_delete='CASCADE', on_update='CASCADE')

        class Meta:
            table_name = "coin_duty_junction"
            schema = "coins"
            indexes = [(('coin_id', 'duty_id'), True)]


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.remove_model('coin_duty_junction')

    migrator.remove_model('duty')

    migrator.remove_model('coin')
