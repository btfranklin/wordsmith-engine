import { Component, join } from "../core.js";

export const spaced = (...parts: Parameters<typeof join>[0]) => join(parts, " ");

export abstract class StatelessComponent extends Component {
  constructor() {
    super();
    Object.freeze(this);
  }
}
