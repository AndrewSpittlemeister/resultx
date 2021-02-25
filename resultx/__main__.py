from resultx import result

@result
def add(a, b) -> int:
    return a + b

def main() -> None:

    ### examine function with a valid result ######################################################
    res = add(10, 10)
    print(res)

    # check if the result has a valid value
    assert res.is_val()

    # grab the value if it is valid, otherwise throw an exception
    assert res.as_val() == 20

    # grab the value if it is valid, otherwise return a default
    assert res.try_val(default=21) == 20

    # grab value if it is valid and use it in a lambda function, otherwise throw an exception
    assert res.as_val_then(lambda x: x + 1) == 21

    # grab value if it is valid, otherwise use default in lambda function
    assert res.try_val_then(lambda x: x + 1, default=21) == 21

    # grab the value value or otherwise call a lambda function with the error value
    assert res.as_val_else(lambda e: print(e)) == 20

    # grab the value otherwise call a lambda function and return its result
    assert res.try_val_else(lambda: "20") == 20

    # check if the result has an error value
    assert not res.is_err()

    # grab the value if it is an error value, otherwise throw an exception
    try:
        err = res.as_err()
    except Exception as e:
        print(f"\tas_err: {e}")

    # grab the value if it is an error value, otherwise return the default provided
    assert res.try_err(default=10) == 10

    ### examine function with an error result #####################################################
    res = add(10, "10")
    print(res)

    # check if the result has a valid value
    assert not res.is_val()

    # grab the value if it is valid, otherwise throw an exception
    try:
        val = res.as_val()
    except Exception as e:
        print(f"\tas_val: {e}")

    # grab the value if it is valid, otherwise return a default
    assert res.try_val(default=21) == 21

    # grab value if it is valid and use it in a lambda function, otherwise throw an exception
    try:
        val = res.as_val_then(lambda x: x + 1)
    except Exception as e:
        print(f"\tas_val_then: {e}")

    # grab value if it is valid, otherwise use default in lambda function
    assert res.try_val_then(lambda x: x + 1, default=21) == 22

    # grab the value value or otherwise call a lambda function with the error value
    assert res.as_val_else(lambda e: print(f"\tas_vel_else: in lambda, e -> {e}")) == None

    # grab the value otherwise call a lambda function and return its result
    assert res.try_val_else(lambda: "2" + "0") == "20"

    # check if the result has an error value
    assert res.is_err()

    # grab the value if it is an error value, otherwise throw an exception
    assert isinstance(res.as_err(), Exception)

    # grab the value if it is an error value, otherwise return the default provided
    assert isinstance(res.try_err(), Exception)


if __name__ == "__main__":
    main()