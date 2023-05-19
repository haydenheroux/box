## box_t

Wraps a value with a flag for if the value has been read (opened) since it was last modified (filled).

struct box_t

Parameters:
 - BOX_VALUE_TYPE value
 - bool opened


## box_fill

Fills a box with a value and closes the box after it is filled.

void box_fill

Parameters:
 - box_t* box
 - BOX_VALUE_TYPE value


## box_open

Opens a box and returns the value inside.

BOX_VALUE_TYPE box_open

Parameters:
 - box_t* box


## box_slice_t

Wraps a buffer of pointers to boxes with the length of the buffer.

struct box_slice_t

Parameters:
 - box_t** boxes
 - box_size_t length


## box_create_slice

Creates a slice of boxes with the specified length.

void box_create_slice

Parameters:
 - box_slice_t* boxes
 - box_size_t length


## box_delete_slice

Deletes a slice of boxes, including deleting each box.

void box_delete_slice

Parameters:
 - box_slice_t* boxes


## box_get

Gets the box occupying the slice at the specified index.

box_t* box_get

Parameters:
 - box_slice_t boxes
 - int index


## box_all_closed

Returns true if all boxes in a slice are closed.

bool box_all_closed

Parameters:
 - box_slice_t boxes


## box_all_opened

Returns true if all boxes in a slice are opened.

bool box_all_opened

Parameters:
 - box_slice_t boxes


## box_count_closed

Counts the number of boxes in a slice that are closed.

int box_count_closed

Parameters:
 - box_slice_t boxes


## box_count_opened

Counts the number of boxes in a slice that are opened.

int box_count_opened

Parameters:
 - box_slice_t boxes


## box_get_match

Gets the first box in a slice that returns true when tested.

box_t* box_get_match

Parameters:
 - box_slice_t boxes
 - bool (*test)(box_t*)


## box_get_matches

Gets all boxes in a slice that return true when tested.

int box_get_matches

Parameters:
 - box_slice_t boxes
 - box_slice_t* matches
 - bool (*test)(box_t*)


## is_negative

Returns true if the box contains a negative value.

bool is_negative

Parameters:
 - box_t* box


## is_positive

Returns true if the box contains a positive value.

bool is_positive

Parameters:
 - box_t* box
