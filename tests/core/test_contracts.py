import pytest
from pydantic import BaseModel

# We will import from launch_engine.core.contracts after we create it
# For now, we expect it to fail because the module doesn't exist
from launch_engine.core.contracts import BaseModuleInput, LaunchModule


def test_base_module_input_is_pydantic_model():
    """Test that BaseModuleInput is a Pydantic BaseModel."""
    assert issubclass(BaseModuleInput, BaseModel)


def test_base_module_input_can_be_subclassed():
    """Test that we can subclass BaseModuleInput and add fields."""

    class TestInput(BaseModuleInput):
        name: str
        age: int

    inp = TestInput(name="test", age=25)
    assert inp.name == "test"
    assert inp.age == 25


def test_base_module_input_validates_types():
    """Test that BaseModuleInput validates types correctly."""

    class TestInput(BaseModuleInput):
        age: int

    # Valid
    inp = TestInput(age=25)
    assert inp.age == 25

    # Invalid
    with pytest.raises(Exception):
        TestInput(age="not an integer")


def test_launch_module_protocol():
    """Test that LaunchModule protocol is defined and can be used."""
    # Check that LaunchModule has the required attributes (as a Protocol, it defines the interface)
    # We can't instantiate a Protocol, but we can check that it is a Protocol by checking for _is_protocol
    # However, for simplicity, we'll just check that we can use it as a base class for a class that we then check.
    # Instead, we'll define a dummy class and check that it has the attributes that the protocol requires.

    class DummyModule:
        name = "dummy"

        async def run(self, input_data: BaseModuleInput) -> BaseModuleInput:
            return input_data

    # Check that DummyModule has the attributes
    assert hasattr(DummyModule, "name")
    assert hasattr(DummyModule, "run")
    # Check that name is a string (we set it to a string)
    assert isinstance(DummyModule.name, str)
    # Check that run is callable
    assert callable(DummyModule.run)

    # Additionally, we can check that LaunchModule is indeed a Protocol by checking its type
    from typing import Protocol

    assert isinstance(LaunchModule, type(Protocol))
