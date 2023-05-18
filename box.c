#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#define BOX_VALUE_TYPE double

// Wraps a value with a flag for if the value has been read (opened) since it was last modified (filled).
typedef struct {
	BOX_VALUE_TYPE value;
	bool opened;
} box_t;

// Fills a box with a value and closes the box after it is filled.
void
box_fill(box_t* box, BOX_VALUE_TYPE value)
{
	box->value = value;
	box->opened = false;
}

// Opens a box and returns the value inside.
BOX_VALUE_TYPE
box_open(box_t* box)
{
	box->opened = true;
	return box->value;
}

typedef unsigned long box_size_t;

// Wraps a buffer of pointers to boxes with the length of the buffer.
typedef struct {
	box_t** boxes;
	box_size_t length;
} box_slice_t;

// Creates a slice of boxes with the specified length.
void
box_create_slice(box_slice_t* boxes, box_size_t length)
{
	assert(boxes->boxes == 0);
	assert(boxes->length == 0);

	boxes->boxes = calloc(length, sizeof(box_t*));

	for (int i = 0; i < length; ++i) {
		boxes->boxes[i] = calloc(1, sizeof(box_t));
	}

	boxes->length = length;
}

// Deletes a slice of boxes, including deleting each box.
void
box_delete_slice(box_slice_t* boxes)
{
	for (int i = 0; i < boxes->length; ++i) {
		free(boxes->boxes[i]);
	}

	free(boxes->boxes);

	boxes->boxes = 0;
	boxes->length = 0;

	assert(boxes->boxes == 0);
}

// Gets the box occupying the slice at the specified index.
box_t*
box_get(box_slice_t boxes, int index)
{
	if (index >= boxes.length) return 0;
	return boxes.boxes[index];
}

// Returns true if all boxes in a slice are closed.
bool
box_all_closed(box_slice_t boxes)
{
	for (int i = 0; i < boxes.length; i++) {
		if (boxes.boxes[i]->opened) return false;
	}
	return true;
}

// Returns true if all boxes in a slice are opened.
bool
box_all_opened(box_slice_t boxes)
{
	for (int i = 0; i < boxes.length; i++) {
		if (boxes.boxes[i]->opened == false) return false;
	}
	return true;
}

// Counts the number of boxes in a slice that are closed.
int
box_count_closed(box_slice_t boxes)
{
	int closed_boxes = 0;
	for (int i = 0; i < boxes.length; ++i) {
		if (boxes.boxes[i]->opened == false) ++closed_boxes;
	}
	return closed_boxes;
}

// Counts the number of boxes in a slice that are opened.
int
box_count_opened(box_slice_t boxes)
{
	int opened_boxes = 0;
	for (int i = 0; i < boxes.length; ++i) {
		if (boxes.boxes[i]->opened) ++opened_boxes;
	}
	return opened_boxes;
}

// Gets the first box in a slice that returns true when tested.
box_t*
box_get_match(box_slice_t boxes, bool (*test)(box_t*))
{
	for (int i = 0; i < boxes.length; ++i) {
		if (test(boxes.boxes[i])) return boxes.boxes[i];
	}
	return 0;
}

// Gets all boxes in a slice that return true when tested.
int
box_get_matches(box_slice_t boxes, box_slice_t* matches, bool (*test)(box_t*))
{
	assert(matches->length >= boxes.length);

	int j = 0;
	for (int i = 0; i < boxes.length; ++i) {
		if (test(boxes.boxes[i])) {
			matches->boxes[j++] = boxes.boxes[i];
		}
	}
	return j;
}

// Returns true if the box contains a negative value.
bool
is_negative(box_t* box)
{
	return box_open(box) < 0;
}

// Returns true if the box contains a positive value.
bool
is_positive(box_t* box)
{
	return box_open(box) > 0;
}

int
main(int argc, char** argv)
{
	box_slice_t boxes = {.boxes = 0, .length = 0};

	printf("sizeof(box_t): %lu\n", sizeof(box_t));
	printf("sizeof(box_slice_t): %lu\n", sizeof(box_slice_t));

	box_create_slice(&boxes, 4);

	box_fill(box_get(boxes, 0), 0);
	box_fill(box_get(boxes, 1), 2);
	box_fill(box_get(boxes, 2), -2);
	box_fill(box_get(boxes, 3), 1);

	printf("closed_boxes: %d\n", box_count_closed(boxes));
	printf("opened_boxes: %d\n", box_count_opened(boxes));

	box_slice_t matches = {.boxes = 0, .length = 0};

	box_create_slice(&matches, 4);

	int num_matches = box_get_matches(boxes, &matches, is_negative);
	for (int i = 0; i < num_matches; ++i) {
		box_fill(box_get(matches, i), 0);
	}

	for (int i = 0; i < boxes.length; ++i) {
		printf("boxes[%d] = %f\n", i, box_open(box_get(boxes, i)));
	}

	printf("closed_boxes: %d\n", box_count_closed(boxes));
	printf("opened_boxes: %d\n", box_count_opened(boxes));

	box_delete_slice(&boxes);

	return 0;
}
