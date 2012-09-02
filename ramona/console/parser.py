import argparse

###

class _parser_base(argparse.ArgumentParser):

	argparser_kwargs = {}
	subparser_kwargs = {}

	def __init__(self):
		argparse.ArgumentParser.__init__(self, **self.argparser_kwargs)

		subparsers = self.add_subparsers(
			dest='subcommand',
			title='subcommands',
			parser_class=argparse.ArgumentParser,
		)
		
		# Adding sub-commands ...
		self.subcommands = {}
		for cmd in self.build_cmdlist():
			subparser = subparsers.add_parser(cmd.name, help=cmd.cmdhelp, **self.subparser_kwargs)
			cmd.init_parser(subparser)
			self.subcommands[cmd.name] = cmd


	def build_cmdlist(self):
		from .cmd import start
		yield start

		from .cmd import stop
		yield stop

		from .cmd import restart
		yield restart

		from .cmd import status
		yield status

		from .cmd import help
		yield help


	def parse(self, argv):
		self.args = self.parse_args(argv)
		

	def execute(self, cnsapp):
		if self.args.subcommand == 'help':
			# Help is given by special treatment as this is actually function of parser itself
			self.print_help()
			return

		return self.subcommands[self.args.subcommand].main(cnsapp, self.args)

#

class argparser(_parser_base):

	def __init__(self):
		_parser_base.__init__(self)

		# Add config file option
		self.add_argument('-c', '--config', metavar="CONFIGFILE", action='append', help='Specify config file(s) to read (this option can be given more times).')

		# Add debug log level option
		self.add_argument('-d', '--debug', action='store_true', help='Enable debug (verbose) output.')

		# Add silent log level option
		self.add_argument('-s', '--silent', action='store_true', help='Enable silent mode of operation (only errors are printed).')


	def build_cmdlist(self):
		for cmd in _parser_base.build_cmdlist(self): yield cmd

		from .cmd import console
		yield console

		from .cmd import server
		yield server

#

class consoleparser(_parser_base):

	argparser_kwargs = {'add_help': False, 'usage': argparse.SUPPRESS}
	subparser_kwargs = {'usage': argparse.SUPPRESS}

	def build_cmdlist(self):
		for cmd in _parser_base.build_cmdlist(self): yield cmd

		from .cmd import exit
		yield exit


	def error(self, message):
		print "Error:", message
		raise SyntaxError()

