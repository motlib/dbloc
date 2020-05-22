# dbloc

`dbloc` is the Django Building Locator. This is a Django based web-application
to manage plans of buildings and link between them. It can e.g. be used for
in-house navigation on a company site.

Currently this is a training application, i.e. I write it to learn django
development and not to provide a feature-complete application.

## License

This project is licensed under the GNU General Public License, version 3. See
`LICENSE` file for the full license text.

## Usage / Setup

Here's a very brief introduction to getting this application running:

```sh
# Build the docker image
make docker

# Start the docker container, by use of Makefile
make docker_run
```
