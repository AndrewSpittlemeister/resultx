from typing import Callable, Any, Union, Optional
from dataclasses import dataclass


@dataclass
class Nothing:
    pass


class Result:

    __slots__ = ["__res", "__is_val"]

    def __init__(self, val_res: Union[Any, Nothing] = Nothing(), err_res: Union[Exception, Nothing] = Nothing()) -> None:
        if isinstance(val_res, Nothing) and isinstance(err_res, Nothing):
            raise Exception("must initiate 'val' or 'err' values")
        elif not isinstance(val_res, Nothing) and not isinstance(err_res, Nothing):
            raise Exception("cannot initiate 'val' and 'err' values at the same time")
        elif not isinstance(val_res, Nothing) and isinstance(err_res, Nothing):
            self.__res: Union[Any, Exception] = val_res
            self.__is_val: bool = True
        elif isinstance(val_res, Nothing) and isinstance(err_res, Exception):
            self.__res: Union[Any, Exception] = err_res
            self.__is_val: bool = False
        else:
            raise NotImplementedError("unreachable")

    @classmethod
    def from_val(cls, x: Any):
        """Builds the result object with a valid value."""

        return cls(val_res=x)

    @classmethod
    def val(cls, x: Any):
        """Builds the result object with a valid value (shorthand for from_val)."""

        return cls(val_res=x)

    @classmethod
    def from_err(cls, e: Exception):
        """Builds the result object with with an error value."""

        return cls(err_res=e)

    @classmethod
    def err(cls, e: Exception):
        """Builds the result object with with an error value (shorthand for from_err)."""

        return cls(err_res=e)

    def __str__(self) -> str:
        """Returns human readable description of the result object and its embedded data.

        Returns:
            str: Result object string representation.
        """

        if self.__is_val:
            return f"Result{type(self.__res)} (Valid) @ addr:{id(self.__res)}"
        else:
            return f"Result{type(self.__res)} (Error) @ addr:{id(self.__res)}"

    ### As-Valid Assumption Methods ###########################################################################################################################

    def is_val(self) -> bool:
        """Returns True if the result object holds a valid value.

        Returns:
            bool: Boolean denoting if the contained value is valid.
        """

        return self.__is_val

    def as_val(self) -> Any:
        """Returns the valid value of the result object if it exists, otherwise throws an exception.

        Returns:
            Any: A valid value.
        """

        if self.__is_val:
            return self.__res
        else:
            raise Exception("cannot use as valid value")

    def try_val(self, default: Optional[Any] = None) -> Optional[Any]:
        """Returns the valid value of the result object if it exists, otherwise returns a default value.

        Args:
            default (Optional[Any], optional): Default value to return. Defaults to None.

        Returns:
            Optional[Any]: Valid value or default provided.
        """

        if self.__is_val:
            return self.__res
        else:
            return default

    def as_val_then(self, func: Callable[[Any], Any]) -> Any:
        """Calls the given function with the value supplied as the argument if it is valid, otherwise will raise an exception.

        Args:
            func (Callable[[Any], Any]): Function to call with the value

        Returns:
            Any: Value returned from the called function.
        """

        if callable(func):
            if self.__is_val:
                return func(self.__res)
            else:
                raise Exception("cannot use as valid value")
        else:
            raise Exception("else clause argument must be callable")

    def try_val_then(self, func: Callable[[Any], Any], default: Optional[Any] = None) -> Any:
        """Calls the given function with the value supplied as the argument if it is valid, otherwise will call the function with the default value.

        Args:
            func (Callable[[Any], Any]): Function to call with the value.
            default (Optional[Any], optional): Default value to call the function with. Defaults to None.

        Returns:
            Any: Value returned from the called function.
        """

        if callable(func):
            if self.__is_val:
                return func(self.__res)
            else:
                return func(default)
        else:
            raise Exception("else clause argument must be callable")

    def as_val_else(self, func: Callable[[Exception], Any]) -> Any:
        """Returns the value if it is valid otherwise will return the result of the function call that takes the error value as an argument.

        Args:
            func (Callable[[Exception], Any]): Function to handle the error value.

        Returns:
            Any: Either the valid value in the result object or the returned value from the function call.
        """

        if callable(func):
            if self.__is_val:
                return self.__res
            else:
                return func(self.__res)
        else:
            raise Exception("else clause argument must be callable")

    def try_val_else(self, func: Callable[[], Any]) -> Any:
        """Returns the value if it is valid, otherwise will return the result of the provided function.

        Args:
            func (Callable[[], Any]): Function to call if the value is not valid.

        Raises:
            Exception: [description]

        Returns:
            Any: Either the valid value in the result object or what is returned from the provided function.
        """

        if callable(func):
            if self.__is_val:
                return self.__res
            else:
                return func()
        else:
            raise Exception("else clause argument must be callable")

    ### As-Error Assumption Methods ###########################################################################################################################

    def is_err(self) -> bool:
        """Returns True if the result object holds an error value.

        Returns:
            bool: Boolean denoting if the contained value is an error value.
        """

        return not self.__is_val

    def as_err(self) -> Exception:
        """Returns the error value of the result object if it exists, otherwise throws an exception.

        Returns:
            Exception: A error value.
        """

        if not self.__is_val:
            return self.__res
        else:
            raise Exception("cannot use as exception")
    
    def try_err(self, default: Optional[Any] = None) -> Union[Optional[Any], Exception]:
        """Returns the error value of the result object if it exists, otherwise returns a default value.

        Args:
            default (Optional[Any], optional): Default value to return. Defaults to None.

        Returns:
            Union[Optional[Any], Exception]: Error value or default provided.
        """

        if not self.__is_val:
            return self.__res
        else:
            return default
