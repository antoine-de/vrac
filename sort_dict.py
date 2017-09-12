from collections import deque
import itertools
import json


def comparator(compare_generator):
    def compare(obj1, obj2):
        """
        To decide that 2 objects are equals, we loop through all values of the
        compare_generator and stop at the first non equals value

        Note: the fillvalue is the value used when a generator is consumed
        (if the 2 generators does not return the same number of elt).
        by setting it to object(), we ensure that it will be !=
        from any values returned by the other generator
        """
        for a, b in itertools.izip_longest(compare_generator(obj1),
                                           compare_generator(obj2),
                                           fillvalue=object()):
            if a != b:
                return -1 if a > b else 1
    return compare

def sort_all_list_dict(response):
    """
    depth first search on a dict.
    sort all list in the dict
    """
    queue = deque()

    def magic_sort(elt):
        to_check = ['uri', 'id', 'label', 'order', 'href']
        for field in to_check:
            if field in elt:
                print 'comparing: ', elt[field]
                yield elt[field]
        yield elt

    def add_elt(elt, first=False):
        if isinstance(elt, (list, tuple)):
            if isinstance(elt, list):
                elt.sort(cmp=comparator(magic_sort))
            for val in elt:
                queue.append(val)
        elif hasattr(elt, 'iteritems'):
            for k, v in elt.iteritems():
                queue.append((k, v))
        elif first:  # for the first elt, we add it even if it is no collection
            queue.append(elt)

    add_elt(response, first=True)
    while queue:
        elem = queue.pop()
        #for list and tuple, the name is the parent's name
        add_elt(elem)

raw_json = """
{
  "query": "http://localhost/v1/coverage/bibus/stop_points/stop_point%3ABIB%3ASP%3ANav504?depth=3",
  "response": {
    "stop_points": [
      {
        "name": "Amiral Ronarc'h",
        "links": [],
        "coord": {
          "lat": "48.395487",
          "lon": "-4.524462"
        },
        "label": "Amiral Ronarc'h (Brest)",
        "equipments": [],
        "administrative_regions": [
          {
            "insee": "29019",
            "name": "Brest",
            "level": 8,
            "coord": {
              "lat": "48.38987538",
              "lon": "-4.487201604"
            },
            "label": "Brest (29200)",
            "id": "admin:29019",
            "zip_code": "29200"
          }
        ],
        "address": {
          "name": "Rue Brahms",
          "house_number": 1,
          "coord": {
            "lat": "48.395487",
            "lon": "-4.524462"
          },
          "label": "1 Rue Brahms (Brest)",
          "administrative_regions": [
            {
              "insee": "29019",
              "name": "Brest",
              "level": 8,
              "coord": {
                "lat": "48.38987538",
                "lon": "-4.487201604"
              },
              "label": "Brest (29200)",
              "id": "admin:29019",
              "zip_code": "29200"
            }
          ],
          "id": "-4.524462;48.395487"
        },
        "id": "stop_point:BIB:SP:Nav504",
        "stop_area": {
          "commercial_modes": [
            {
              "name": "Bus",
              "id": "commercial_mode:bus"
            },
            {
              "name": "mode commercial par d\u00e9faut",
              "id": "commercial_mode:default_commercial_mode"
            }
          ],
          "name": "Amiral Ronarc'h",
          "links": [],
          "physical_modes": [
            {
              "name": "mode physique par d\u00e9faut",
              "id": "physical_mode:default_physical_mode"
            },
            {
              "name": "Bus",
              "id": "physical_mode:Bus"
            }
          ],
          "coord": {
            "lat": "48.395479",
            "lon": "-4.524068"
          },
          "label": "Amiral Ronarc'h (Brest)",
          "administrative_regions": [
            {
              "insee": "29019",
              "name": "Brest",
              "level": 8,
              "coord": {
                "lat": "48.38987538",
                "lon": "-4.487201604"
              },
              "label": "Brest (29200)",
              "id": "admin:29019",
              "zip_code": "29200"
            }
          ],
          "timezone": "Europe/Paris",
          "id": "stop_area:BIB:SA:10"
        }
      }
    ],
    "pagination": {
      "start_page": 0,
      "items_on_page": 1,
      "items_per_page": 25,
      "total_result": 1
    },
    "feed_publishers": [
      {
        "url": "",
        "id": "bibus",
        "license": "",
        "name": ""
      }
    ],
    "links": [
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/commercial_modes/{commercial_modes.id}",
        "type": "commercial_modes",
        "rel": "commercial_modes",
        "templated": true
      },
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/stop_areas/{stop_area.id}",
        "type": "stop_area",
        "rel": "stop_areas",
        "templated": true
      },
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/physical_modes/{physical_modes.id}",
        "type": "physical_modes",
        "rel": "physical_modes",
        "templated": true
      },
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/addresses/{address.id}",
        "type": "address",
        "rel": "addresses",
        "templated": true
      },
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/stop_points/{stop_points.id}",
        "type": "stop_points",
        "rel": "stop_points",
        "templated": true
      },
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/stop_points/stop_point:BIB:SP:Nav504",
        "type": "first",
        "templated": false
      }
    ],
    "disruptions": []
  },
  "full_response": {
    "stop_points": [
      {
        "name": "Amiral Ronarc'h",
        "links": [],
        "coord": {
          "lat": "48.395487",
          "lon": "-4.524462"
        },
        "label": "Amiral Ronarc'h (Brest)",
        "equipments": [],
        "administrative_regions": [
          {
            "insee": "29019",
            "name": "Brest",
            "level": 8,
            "coord": {
              "lat": "48.38987538",
              "lon": "-4.487201604"
            },
            "label": "Brest (29200)",
            "id": "admin:29019",
            "zip_code": "29200"
          }
        ],
        "address": {
          "name": "Rue Brahms",
          "house_number": 1,
          "coord": {
            "lat": "48.395487",
            "lon": "-4.524462"
          },
          "label": "1 Rue Brahms (Brest)",
          "administrative_regions": [
            {
              "insee": "29019",
              "name": "Brest",
              "level": 8,
              "coord": {
                "lat": "48.38987538",
                "lon": "-4.487201604"
              },
              "label": "Brest (29200)",
              "id": "admin:29019",
              "zip_code": "29200"
            }
          ],
          "id": "-4.524462;48.395487"
        },
        "id": "stop_point:BIB:SP:Nav504",
        "stop_area": {
          "commercial_modes": [
            {
              "name": "Bus",
              "id": "commercial_mode:bus"
            },
            {
              "name": "mode commercial par d\u00e9faut",
              "id": "commercial_mode:default_commercial_mode"
            }
          ],
          "name": "Amiral Ronarc'h",
          "links": [],
          "physical_modes": [
            {
              "name": "mode physique par d\u00e9faut",
              "id": "physical_mode:default_physical_mode"
            },
            {
              "name": "Bus",
              "id": "physical_mode:Bus"
            }
          ],
          "coord": {
            "lat": "48.395479",
            "lon": "-4.524068"
          },
          "label": "Amiral Ronarc'h (Brest)",
          "administrative_regions": [
            {
              "insee": "29019",
              "name": "Brest",
              "level": 8,
              "coord": {
                "lat": "48.38987538",
                "lon": "-4.487201604"
              },
              "label": "Brest (29200)",
              "id": "admin:29019",
              "zip_code": "29200"
            }
          ],
          "timezone": "Europe/Paris",
          "id": "stop_area:BIB:SA:10"
        }
      }
    ],
    "pagination": {
      "items_per_page": 25,
      "items_on_page": 1,
      "start_page": 0,
      "total_result": 1
    },
    "disruptions": [],
    "links": [
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/commercial_modes/{commercial_modes.id}",
        "type": "commercial_modes",
        "rel": "commercial_modes",
        "templated": true
      },
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/stop_areas/{stop_area.id}",
        "type": "stop_area",
        "rel": "stop_areas",
        "templated": true
      },
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/physical_modes/{physical_modes.id}",
        "type": "physical_modes",
        "rel": "physical_modes",
        "templated": true
      },
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/addresses/{address.id}",
        "type": "address",
        "rel": "addresses",
        "templated": true
      },
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/stop_points/{stop_points.id}",
        "type": "stop_points",
        "rel": "stop_points",
        "templated": true
      },
      {
        "href": "http://SERVER_ADDR/v1/coverage/bibus/stop_points/stop_point:BIB:SP:Nav504",
        "type": "first",
        "templated": false
      }
    ],
    "feed_publishers": [
      {
        "url": "",
        "id": "bibus",
        "license": "",
        "name": ""
      }
    ]
  }
}

"""

raw_json = """
{
  "full_response": {
    "stop_points": [
      {
        "name": "Amiral Ronarc'h",
        "links": [],
        "coord": {
          "lat": "48.395487",
          "lon": "-4.524462"
        },
        "label": "Amiral Ronarc'h (Brest)",
        "equipments": [],
        "administrative_regions": [
          {
            "insee": "29019",
            "name": "Brest",
            "level": 8,
            "coord": {
              "lat": "48.38987538",
              "lon": "-4.487201604"
            },
            "label": "Brest (29200)",
            "id": "admin:29019",
            "zip_code": "29200"
          }
        ],
        "id": "stop_point:BIB:SP:Nav504",
        "stop_area": {
          "commercial_modes": [
            {
              "name": "Bus",
              "id": "commercial_mode:bus"
            },
            {
              "name": "mode commercial par d\u00e9faut",
              "id": "commercial_mode:default_commercial_mode"
            }
          ],
          "name": "Amiral Ronarc'h",
          "links": [],
          "physical_modes": [
            {
              "name": "mode physique par d\u00e9faut",
              "id": "physical_mode:default_physical_mode"
            },
            {
              "name": "Bus",
              "id": "physical_mode:Bus"
            }
          ],
          "coord": {
            "lat": "48.395479",
            "lon": "-4.524068"
          },
          "label": "Amiral Ronarc'h (Brest)"

        }
      }
    ]
  }
}
"""
d = json.loads(raw_json)

sort_all_list_dict(d)

print json.dumps(d, indent=2)
