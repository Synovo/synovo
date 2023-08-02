import _ from 'lodash';

const self_closing: string[] = ['img', 'meta', 'link', 'input', 'embed', 'br', 'hr', 'source'];

const stringify_props = (props?: Record<string, any>) => props ? Object.entries(props).filter(i => i[0] != 'children').map(([a, i]) => ` ${a}="${i}"`).join('') : '';

/**
 * Used to override how tags are rendered
 */
const tags: Record<string, <T extends JSX.Props>(props?: T) => string | Promise<string>> = {
    ..._.chain(self_closing)
        .map(i => [i, (props: JSX.Props) => `<${i}${stringify_props(props)} />`])
        .fromPairs()
        .value(),
    html: async <T extends JSX.Props>(props?: T) => `<!DOCTYPE html><html${stringify_props(props)}>${await render(props?.children)}</html>`
};

export function createElement<T extends JSX.Props>(el: string | ((props: T) => JSX.Element<any>), props: T = {} as any): JSX.Element<T> {
    return {
        async render(): Promise<string> {
            if (!el)
                return '';
            else if (typeof el == 'string')
                if (el in tags)
                    return await tags[el](props);
                else
                    return `<${el}${stringify_props(props)}>${await render(props?.children)}</${el}>`;
            else
                return await (await el(props)).render();
        },
        set_prop<Name extends keyof T>(name: Name, value: T[Name]): JSX.Element<T> {
            return createElement(el, { ...props, [name]: value });
        }
    }
}

export const render = async (els?: string | JSX.Element<any> | JSX.Element<any>[]) => els ? await Promise.all((els ? Array.isArray(els) ? els : [els] : [])
    .filter(i => i !== null)
    .map(async i => ['string', 'number', 'boolean', 'bigint', 'function'].includes(typeof i) ? i : await (i as any)?.render?.() ?? ''))
    .then(ans => ans.join('')) : '';

export function Fragment<K extends JSX.Props, T extends JSX.WithChildren<K>>(props: T): JSX.Element<K> {
    return {
        async render(): Promise<string> {
            return await render(props.children);
        },
        set_prop<Name extends keyof T>(name: Name, value: any): JSX.Element<K> {
            return Fragment({ ...props, [name]: value });
        }
    }
}

export declare namespace JSX {
    interface Element<T extends JSX.Props = JSX.Props> {
        render(): Promise<string>,
        set_prop<Name extends keyof T>(name: Name, value: T[Name]): JSX.Element<T>
    }

    interface IntrinsicElements {
        [key: string]: any
    }

    type Props = { [K in string]: any } & { children?: string | JSX.Element<any> | JSX.Element<any>[] };

    export type WithProps<T extends JSX.Props> = T;
    export type Children = string | JSX.Element<any> | JSX.Element<any>[];
    export type WithChildren<T extends JSX.Props> = T & { children?: Children };
}

export const jsx = createElement;
export const jsxs = createElement;
export const jsxDEV = createElement;