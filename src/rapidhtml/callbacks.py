import json

from typing import Literal, Optional, Callable

from dataclasses import dataclass


@dataclass
class RapidHTMLCallback:
    """
    A class to represent a callback function. Abstracts away most of the
    HTMX attributes and provides a more Pythonic interface.


    Attributes:

        func (Callable): The callback function.

        method (Optional[Literal["get", "post", "delete", "patch", "put"]]): The
            HTTP method to use for the callback.

        on (Optional[tuple[str, str]]): Handle events with inline scripts on
            elements

        push_url (Optional[str]): Push a URL into the browser location bar to
            create history.

        select (Optional[str]): Select content to swap in from a response.

        select_oob (Optional[str]): Select content to swap in from a response,
            somewhere other than the target (out of band).

        swap (Optional[Literal["innerHTML", "outerHTML", "textContent",
            "beforebegin", "afterbegin", "beforeend", "afterend", "delete",
            "none"]]): Controls how content will swap in.

        swap_oob (Optional[Literal["innerHTML", "outerHTML", "textContent",
            "beforebegin", "afterbegin", "beforeend", "afterend", "delete",
            "none"]]): Mark element to swap in from a response (out of band).

        target (Optional[str]): Specifies the target element to be swapped.

        trigger (Optional[str]): Specifies the event that triggers the request.

        vals (Optional[dict]): Add values to submit with the request (JSON format).

        boost (Optional[bool]): Add progressive enhancement for links and forms.

        confirm (Optional[str]): Shows a confirm() dialog before issuing a request.

        disable (Optional[bool]): Disables htmx processing for the given node and
            any children nodes.

        disabled_elt (Optional[str]): Adds the disabled attribute to the specified
            elements while a request is in flight.

        disinherit (Optional[str]): Control and disable automatic attribute
            inheritance for child nodes.

        encoding (Optional[str]): Changes the request encoding type.

        ext (Optional[str]): Extensions to use for this element.

        headers (Optional[dict]): Adds to the headers that will be submitted with
            the request.

        history (Optional[bool]): Prevent sensitive data being saved to the history
            cache.

        history_elt (Optional[bool]): The element to snapshot and restore during
            history navigation.

        include (Optional[str]): Include additional data in requests.

        indicator (Optional[str]): The element to put the htmx-request class on
            during the request.

        inherit (Optional[str]): Control and enable automatic attribute inheritance
            for child nodes if it has been disabled by default.

        params (Optional[str]): Filters the parameters that will be submitted with
            a request.

        preserve (Optional[bool]): Specifies elements to keep unchanged between
            requests.

        prompt (Optional[str]): Shows a prompt() before submitting a request.

        replace_url (Optional[str]): Replace the URL in the browser location bar.

        request (Optional[str | dict]): Configures various aspects of the request.

        sync (Optional[Literal["drop", "abort", "replace", "queue", "queue first",
            "queue last", "queue all"]]): Control how requests made by different
            elements are synchronized.

        validate (Optional[bool]): Force elements to validate themselves before a
            request.

    More information on the HTMX attributes can be found here:
        https://htmx.org/reference/


    """

    func: Callable
    method: Optional[Literal["get", "post", "delete", "patch", "put"]] = "get"
    on: Optional[tuple[str, str]] = None
    push_url: Optional[str] = None
    select: Optional[str] = None
    select_oob: Optional[str] = None
    swap: Optional[
        Literal[
            "innerHTML",
            "outerHTML",
            "textContent",
            "beforebegin",
            "afterbegin",
            "beforeend",
            "afterend",
            "delete",
            "none",
        ]
    ] = "innerHTML"
    swap_oob: Optional[
        Literal[
            "innerHTML",
            "outerHTML",
            "textContent",
            "beforebegin",
            "afterbegin",
            "beforeend",
            "afterend",
            "delete",
            "none",
        ]
    ] = None
    target: Optional[str] = None
    trigger: Optional[str] = None
    vals: Optional[dict] = None
    boost: Optional[bool] = None
    confirm: Optional[str] = None
    disable: Optional[bool] = None
    disabled_elt: Optional[str] = None
    disinherit: Optional[str] = None
    encoding: Optional[str] = None
    ext: Optional[str] = None
    headers: Optional[dict] = None
    history: Optional[bool] = None
    history_elt: Optional[bool] = None
    include: Optional[str] = None
    indicator: Optional[str] = None
    inherit: Optional[str] = None
    params: Optional[str] = None
    preserve: Optional[bool] = None
    prompt: Optional[str] = None
    replace_url: Optional[str] = None
    request: Optional[str | dict] = None
    sync: Optional[
        Literal[
            "drop",
            "abort",
            "replace",
            "queue",
            "queue first",
            "queue last",
            "queue all",
        ]
    ] = None
    validate: Optional[bool] = None

    def get_data(self) -> tuple[Callable, str, dict]:
        """Get the data of the callback.

        Returns:
            tuple[Callable, str, dict]: The function, method, and attributes of
            the callback.
        """
        attrs = {}
        if self.on:
            event = self.on[0]
            attrs[f"hx_on:{event}"] = self.on[1]
        if self.push_url:
            attrs["hx_push_url"] = self.push_url
        if self.select:
            attrs["hx_select"] = self.select
        if self.select_oob:
            attrs["hx_select_oob"] = self.select_oob
        if self.swap:
            attrs["hx_swap"] = self.swap
        if self.swap_oob:
            attrs["hx_swap_oob"] = self.swap_oob
        if self.target:
            attrs["hx_target"] = self.target
        if self.trigger:
            attrs["hx_trigger"] = self.trigger
        if self.vals:
            attrs["hx_vals"] = json.dump(self.vals)
        if self.boost:
            attrs["hx_boost"] = "true" if self.boost else "false"
        if self.confirm:
            attrs["hx_confirm"] = self.confirm
        if self.disable:
            attrs["hx_disable"] = self.disable
        if self.disabled_elt:
            attrs["hx_disabled_elt"] = self.disabled_elt
        if self.disinherit:
            attrs["hx_disinherit"] = self.disinherit
        if self.encoding:
            attrs["hx_encoding"] = self.encoding
        if self.ext:
            attrs["hx_ext"] = self.ext
        if self.headers:
            attrs["hx_headers"] = json.dump(self.headers)
        if self.history:
            attrs["hx_history"] = "true" if self.history else "false"
        if self.history_elt:
            attrs["hx_history_elt"] = self.history_elt
        if self.include:
            attrs["hx_include"] = self.include
        if self.indicator:
            attrs["hx_indicator"] = self.indicator
        if self.inherit:
            attrs["hx_inherit"] = self.inherit
        if self.params:
            attrs["hx_params"] = self.params
        if self.preserve:
            attrs["hx_preserve"] = self.preserve
        if self.prompt:
            attrs["hx_prompt"] = self.prompt
        if self.replace_url:
            attrs["hx_replace_url"] = self.replace_url
        if self.request:
            attrs["hx_request"] = (
                self.request
                if isinstance(self.request, str)
                else json.dump(self.request)
            )
        if self.sync:
            attrs["hx_sync"] = self.sync
        if self.validate:
            attrs["hx_validate"] = "true" if self.validate else "false"
        return self.func, self.method, attrs
