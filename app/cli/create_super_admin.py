"""Create the single Super Admin account.

Usage:
    python -m app.cli.create_super_admin --email admin@example.com --full-name "Platform Admin"

The password is read from SUPER_ADMIN_PASSWORD or prompted for without echo,
so it never appears in shell history or process arguments.
"""

import argparse
import getpass
import os
import sys
from collections.abc import Callable, Sequence

from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from app.db.session import get_session_factory
from app.schemas.user import Email, FullName, Password
from app.services.errors import ConflictError
from app.services.registration_service import RegistrationService


class SuperAdminInput(BaseModel):
    email: Email
    full_name: FullName
    password: Password


def _read_password() -> str:
    from_env = os.environ.get("SUPER_ADMIN_PASSWORD")
    if from_env:
        return from_env
    password = getpass.getpass("Password: ")
    if password != getpass.getpass("Repeat password: "):
        raise SystemExit("Passwords do not match")
    return password


def main(
    argv: Sequence[str] | None = None,
    session_factory: Callable[[], Session] | None = None,
    read_password: Callable[[], str] = _read_password,
) -> int:
    parser = argparse.ArgumentParser(description="Create the Super Admin account.")
    parser.add_argument("--email", required=True)
    parser.add_argument("--full-name", required=True)
    args = parser.parse_args(argv)

    try:
        data = SuperAdminInput(email=args.email, full_name=args.full_name, password=read_password())
    except ValidationError as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)
        return 2

    session = (session_factory or get_session_factory())()
    try:
        user = RegistrationService(session).create_super_admin(
            email=data.email, full_name=data.full_name, password=data.password
        )
    except ConflictError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    finally:
        session.close()

    print(f"Super Admin created: {user.email}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
