import click
from datetime import datetime
from gesetze_crawler import gesetze_im_internet_crawler

@click.group()
def cli():
    """A CLI with three subprograms: gii, bgbl, and dip."""
    pass

@cli.command()
@click.argument('law_text', type=str)
@click.argument('output_dir', type=str)
@click.option('--timestamp', type=str, help="A timestamp in the format YYYYMMDDHHMMSS. Also only year or year+month, etc. possible.")
def gii(law_text, output_dir, timestamp):
    if timestamp:
        gesetze_im_internet_crawler.crawl_gesetze_im_internet_wayback(law_text, timestamp, output_dir)
    else:
        gesetze_im_internet_crawler.crawl_gesetze_im_internet(law_text, output_dir)

@cli.command()
@click.argument('input_param')
def bgbl(input_param):
    """Subprogram that accepts an INTEGER or DATE-TIME parameter."""
    try:
        # Try to parse as an integer
        int_param = int(input_param)
        click.echo(f"You passed the integer: {int_param}")
    except ValueError:
        try:
            # Try to parse as a datetime
            date_param = datetime.strptime(input_param, '%Y-%m-%d')
            click.echo(f"You passed the date: {date_param.strftime('%Y-%m-%d')}")
        except ValueError:
            click.echo("Error: input must be either an integer or a date in the format YYYY-MM-DD.", err=True)

@cli.command()
@click.argument('first_int', type=int)
@click.argument('second_int', type=int)
def dip(first_int, second_int):
    """Subprogram that accepts TWO INTEGER parameters."""
    click.echo(f"You passed the integers: {first_int} and {second_int}")

if __name__ == '__main__':
    cli()
