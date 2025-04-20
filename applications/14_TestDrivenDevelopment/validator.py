def validate_input(data, expected_size):
    """
    Validate that the input is a list of the expected size.
    Raise an error if it's not valid.
    """
    if not isinstance(data, list):
        raise TypeError("Input must be a list.")
    if len(data) != expected_size:
        raise ValueError(f"Expected input of length {expected_size}, got {len(data)}.")
    return True  # If it passes all checks
