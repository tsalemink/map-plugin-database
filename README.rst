===================
MAP Plugin Database
===================

.. _MAP Client: https://github.com/MusculoskeletalAtlasProject/mapclient
.. _MAP Plugin Database: https://github.com/MusculoskeletalAtlasProject/map-plugin-database

The `MAP Client`_ is a cross-platform, plugin-based framework for managing workflows. Since the Plugin lies at the heart of the MAP
framework, the ability to easily find and share MAP plugins is an important aspect of the MAP-Client's usability.

The `MAP Plugin Database`_ contains basic information about all of the known, published MAP-Client plugins. The primary use of this
database is to allow users of the MAP-Client to search for and install MAP-Client plugins directly from within the MAP-Client itself,
rather than having to install plugins manually. Specifically, the *Plugin Finder* tool can be found in the MAP-Client application under
the *Tools* menu dropdown.

MAP-Client users are able to submit their own MAP plugins to the MAP Plugin Database. Currently the recommended process for doing this is
to submit an issue in the `MAP Plugin Database`_ GitHub repository. The issue should be tagged with the *add-plugin* label. The body of the
issue submission should contain only the GitHub repository path of the plugin to be added; this path should be in the format:
*{organization}/{repository}*, for example: *mapclient-plugins/pointsourcestep*.

Editing database entries and triggering the automated processes to update this database are restricted to repository maintainers.