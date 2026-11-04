#!/usr/bin/env python3
"""CLI for prospect management."""

from __future__ import annotations

import argparse
import sys

from .models import Prospect
from .storage import import_from_csv, load_prospects, save_prospects


def cmd_add(args: argparse.Namespace) -> int:
    """Add a new prospect."""
    prospects = load_prospects(args.file)
    prospect = Prospect(
        company_name=args.company,
        industry=args.industry,
        city=args.city,
        website=args.website,
        contact_name=args.contact,
        notes=args.notes,
    )
    prospects.append(prospect)
    save_prospects(prospects, args.file)
    print(f"Added prospect: {prospect}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List all prospects."""
    prospects = load_prospects(args.file)
    if not prospects:
        print("No prospects found.")
        return 0
    for p in prospects:
        print(f"  {p}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    """Check for duplicates."""
    prospects = load_prospects(args.file)
    duplicates: list[tuple[int, int]] = []
    for i, p1 in enumerate(prospects):
        for j, p2 in enumerate(prospects):
            if i < j and p1.matches_duplicate_rule(p2):
                duplicates.append((i, j))
    if duplicates:
        print(f"Found {len(duplicates)} duplicate pairs:")
        for i, j in duplicates:
            print(f"  {i} and {j}: {prospects[i]} | {prospects[j]}")
        return 1
    print("No duplicates found.")
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    """Import prospects from CSV."""
    imported = import_from_csv(args.csv_file)
    existing = load_prospects(args.file)
    all_prospects = existing + imported
    save_prospects(all_prospects, args.file)
    print(f"Imported {len(imported)} prospects from {args.csv_file}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    """Export prospects to JSON."""
    prospects = load_prospects(args.file)
    save_prospects(prospects, args.output)
    print(f"Exported {len(prospects)} prospects to {args.output}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="prospect",
        description="Manage lead prospects for Numu Tech",
    )
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new prospect")
    add_parser.add_argument(
        "-f", "--file", default="prospects.json", help="Data file path"
    )
    add_parser.add_argument("company", help="Company name")
    add_parser.add_argument("industry", help="Industry")
    add_parser.add_argument("city", help="City")
    add_parser.add_argument("--website", help="Website URL")
    add_parser.add_argument("--contact", help="Contact name")
    add_parser.add_argument("--notes", help="Notes")

    # Import command
    import_parser = subparsers.add_parser("import", help="Import prospects from CSV")
    import_parser.add_argument("-f", "--file", default="prospects.json", help="JSON file path")
    import_parser.add_argument("csv_file", help="CSV file to import")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export prospects to JSON")
    export_parser.add_argument("-f", "--file", default="prospects.json", help="JSON file path")
    export_parser.add_argument("output", help="Output JSON file")

    # List command
    list_parser = subparsers.add_parser("list", help="List all prospects")
    list_parser.add_argument(
        "-f", "--file", default="prospects.json", help="Data file path"
    )

    # Check duplicates
    check_parser = subparsers.add_parser(
        "check", help="Check for duplicate prospects"
    )
    check_parser.add_argument(
        "-f", "--file", default="prospects.json", help="Data file path"
    )

    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 1

    cmd = globals().get(f"cmd_{args.command}")
    if cmd is None:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1
    return cmd(args)


if __name__ == "__main__":
    sys.exit(main())