from __future__ import division
import sys
import fiona
import argparse
import shapely.geometry

def parse_args(argv):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    parser.add_argument("-p", "--property-to-half")
    parser.add_argument("-c", "--output-column", default="half")

    args = parser.parse_args(argv)

    return args


def open_input_source(filename):
    results = []
    with fiona.open(filename) as source:
        for record in source:
            results.append(record)
        meta = source.meta

    return results, meta

def write_shapefile(filename, objects, metadata):
    with fiona.open(filename, 'w', driver=metadata['driver'], crs=metadata['crs'], schema=metadata['schema']) as output:
        for obj in objects:
            output.write(obj)


def add_output_column(shapes, fileformat_meta, column_name):
    if column_name in fileformat_meta['schema']['properties']:
        raise ValueError()

    fileformat_meta['schema']['properties'][column_name] = 'int'

    for shape in shapes:
        shape['properties'][column_name] = 0

    return shapes, fileformat_meta

def allocate_shapes(shapes, input_column_name, output_column_name):
    shapes_by_id = {shape['id']: shape for shape in shapes}
    areas = {shape['id']: shapely.geometry.shape(shape['geometry']).area for shape in shapes}
    densities = {shape['id']: shape['properties'][input_column_name] / areas[shape['id']] for shape in shapes}
    total = sum(shape['properties'][input_column_name] for shape in shapes)
    assert total > 0
    half = total / 2
    so_far = 0
    first_half_ids = set()
    for shape in sorted(shapes, key=lambda shape: (shape['properties'][input_column_name] / shapely.geometry.shape(shape['geometry']).area) ):
        so_far += shape['properties'][input_column_name]
        shape['properties'][output_column_name] = 1
        if so_far > half:
            break

    return shapes




def main(argv):
    args = parse_args(argv)
    shapes, fileformat_meta = open_input_source(args.input)
    shapes, fileformat_meta = add_output_column(shapes, fileformat_meta, args.output_column)
    shapes = allocate_shapes(shapes, args.property_to_half, args.output_column)
    write_shapefile(args.output, shapes, fileformat_meta)

if __name__ == '__main__':
    main(sys.argv[1:])
