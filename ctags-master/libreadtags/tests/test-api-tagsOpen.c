/*
*   Copyright (c) 2020, Masatake YAMATO
*
*   This source code is released into the public domain.
*
*   Testing tagsOpen() API function
*/

#include "readtags.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


static int
check_info (tagFileInfo *info, tagFileInfo *expected)
{

	fprintf (stderr, "inspecting info->file.format...");
	if (info->file.format != expected->file.format)
	{
		fprintf (stderr, "unexpected result: %d\n", info->file.format);
		return 1;
	}
	fprintf (stderr, "ok\n");

	fprintf (stderr, "inspecting info->file.sort...");
	if (info->file.sort != expected->file.sort)
	{
		fprintf (stderr, "unexpected result: %d\n", info->file.sort);
		return 1;
	}
	fprintf (stderr, "ok\n");

	fprintf (stderr, "inspecting info->program.author...");
	if (strcmp (info->program.author, expected->program.author))
	{
		fprintf (stderr, "unexpected result: %s\n", info->program.author);
		return 1;
	}
	fprintf (stderr, "ok\n");

	fprintf (stderr, "inspecting info->program.name...");
	if (strcmp (info->program.name, expected->program.name))
	{
		fprintf (stderr, "unexpected result: %s\n", info->program.name);
		return 1;
	}
	fprintf (stderr, "ok\n");

	fprintf (stderr, "inspecting info->program.url...");
	if (strcmp (info->program.url, expected->program.url))
	{
		fprintf (stderr, "unexpected result: %s\n", info->program.url);
		return 1;
	}
	fprintf (stderr, "ok\n");

	fprintf (stderr, "inspecting info->program.version...");
	if (strcmp (info->program.version, expected->program.version))
	{
		fprintf (stderr, "unexpected result: %s\n", expected->program.version);
		return 1;
	}
	fprintf (stderr, "ok\n");

	return 0;
}

int
main (void)
{
	char *srcdir = getenv ("srcdir");
	if (srcdir)
	{
		if (chdir (srcdir) == -1)
		{
			perror ("chdir");
			return 99;
		}
	}

	tagFile *t;
	tagFileInfo info;

	const char *tags0 = "./no-such-file.tags";
	fprintf (stderr, "opening no-existing tags file...");
	t = tagsOpen (tags0, &info);
	if (! (t == NULL
		   && info.status.opened == 0
		   && info.status.error_number != 0))
	{
		fprintf (stderr, "unexpected result (t: %p, opened: %d, error_number: %d)\n",
				 t, info.status.opened, info.status.error_number);
		return 1;
	}
	fprintf (stderr, "ok\n");

	fprintf (stderr, "opening no-existing tags file with NULL tagFileInfo...");
	t = tagsOpen (tags0, NULL);
	if (t != NULL)
	{
		fprintf (stderr, "unexpected result (t: %p)\n", t);
		return 1;
	}
	fprintf (stderr, "ok\n");

	tagFileInfo expected1 = {
		.file.format = 2,
		.file.sort = TAG_SORTED,
		.program.author = "Darren Hiebert",
		.program.name = "Exuberant Ctags",
		.program.url = "http://ctags.sourceforge.net",
		.program.version = "5.8",
	};
	const char *tags1 = "./api-tagsOpen-ectags.tags";
	fprintf (stderr, "opening an existing tags file...");
	t = tagsOpen (tags1, &info);
	if (t == NULL
		|| info.status.opened == 0)
	{
		fprintf (stderr, "unexpected result (t: %p, opened: %d)\n",
				 t, info.status.opened);
		return 1;
	}
	fprintf (stderr, "ok\n");


	if (check_info (&info, &expected1) != 0)
		return 1;

	fprintf (stderr, "closing the tag file...");
	if (tagsClose (t) != TagSuccess)
	{
		fprintf (stderr, "unexpected result\n");
		return 1;
	}
	fprintf (stderr, "ok\n");

	fprintf (stderr, "opening an existing tags file with NULL tagFileInfo...");
	t = tagsOpen (tags1, NULL);
	if (t == NULL)
	{
		fprintf (stderr, "unexpected result\n");
		return 1;
	}
	fprintf (stderr, "ok\n");

	fprintf (stderr, "closing the tag file...");
	if (tagsClose (t) != TagSuccess)
	{
		fprintf (stderr, "unexpected result\n");
		return 1;
	}
	fprintf (stderr, "ok\n");


	return 0;
}
