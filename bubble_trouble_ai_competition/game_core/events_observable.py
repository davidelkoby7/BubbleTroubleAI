from typing import Type

from bubble_trouble_ai_competition.utils.constants import Events, ALL_EVENTS_LIST

class EventsObservable:
    """
    An observable object that all observers can subscribe to in order to get notified about things in the game.
    """

    def __init__(self) -> None:
        """
        Initialize the observable object to have no observers.
        """
        self.observable_events = {}

        for event in ALL_EVENTS_LIST:
            self.observable_events[event] = []
        
        print (self.observable_events)
    

    def add_observer(self, eventType: Events, observer) -> None:
        """
        Add the given observer to the observable object.

        Args:
            observer: The observer to add to the observable object.
        """
        self.observable_events[eventType].append(observer)
    

    def remove_observer(self, observer, eventType: Events) -> None:
        """
        Remove the given observer from the observable object.

        Args:
            observer (Observer): The observer to remove from the observable object.
            eventType (Events): The event type to remove the observer from.
        """
        if (self.observable_events[eventType].count(observer) > 0):
            self.observable_events[eventType].remove(observer)


    def notify_observers(self, event, *args, **kwargs) -> None:
        """
        Notify all the observers of the given event.

        Args:
            event (Events): The event to notify the observers of.
            *args: The arguments to pass to the observers.
            **kwargs: The keyword arguments to pass to the observers.
        """
        for observer in self.observable_events[event]:
            observer(*args, **kwargs)
