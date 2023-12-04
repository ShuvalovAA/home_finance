<%!
import re

%>"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}
<%
    db_names = config.get_main_option("databases")
%>

def upgrade():
% for db_name in re.split(r',\s*', db_names):
    upgrade_${db_name}()
% endfor


def downgrade():
% for db_name in re.split(r',\s*', db_names):
    downgrade_${db_name}()
% endfor




## generate an "upgrade_<xyz>() / downgrade_<xyz>()" function
## for each database name in the ini file.

% for db_name in re.split(r',\s*', db_names):

def upgrade_${db_name}():
    ${context.get("%s_upgrades" % db_name, "pass")}


def downgrade_${db_name}():
    ${context.get("%s_downgrades" % db_name, "pass")}

% endfor
