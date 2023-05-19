## struct box_t

Wraps a value with a flag for if the value has been read (opened) since it was last modified (filled).

Parameters:
 - BOX_VALUE_TYPE value
 - bool opened


## void box_fill

Fills a box with a value and closes the box after it is filled.

Parameters:
 - box_t* box
 - BOX_VALUE_TYPE value


## BOX_VALUE_TYPE box_open

Opens a box and returns the value inside.

Parameters:
 - box_t* box


## struct box_slice_t

Wraps a buffer of pointers to boxes with the length of the buffer.

Parameters:
 - box_t** boxes
 - box_size_t length


## void box_create_slice

Creates a slice of boxes with the specified length.

Parameters:
 - box_slice_t* boxes
 - box_size_t length


## void box_delete_slice

Deletes a slice of boxes, including deleting each box.

Parameters:
 - box_slice_t* boxes


## box_t* box_get

Gets the box occupying the slice at the specified index.

Parameters:
 - box_slice_t boxes
 - int index


## bool box_all_closed

Returns true if all boxes in a slice are closed.

Parameters:
 - box_slice_t boxes


## bool box_all_opened

Returns true if all boxes in a slice are opened.

Parameters:
 - box_slice_t boxes


## int box_count_closed

Counts the number of boxes in a slice that are closed.

Parameters:
 - box_slice_t boxes


## int box_count_opened

Counts the number of boxes in a slice that are opened.

Parameters:
 - box_slice_t boxes


## box_t* box_get_match

Gets the first box in a slice that returns true when tested.

Parameters:
 - box_slice_t boxes
 - bool (*test)(box_t*)


## int box_get_matches

Gets all boxes in a slice that return true when tested.

Parameters:
 - box_slice_t boxes
 - box_slice_t* matches
 - bool (*test)(box_t*)


## bool is_negative

Returns true if the box contains a negative value.

Parameters:
 - box_t* box


## bool is_positive

Returns true if the box contains a positive value.

Parameters:
 - box_t* box
