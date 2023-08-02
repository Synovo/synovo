import fs from 'node:fs/promises';
import module from 'node:module';
import { iterSync } from '@j-cake/jcake-utils/iter';

const dir = import.meta.url.match(/^file:\/\/(.*)\/[^\/]*$/)[1] ?? process.cwd();
const req = module.createRequire(dir);

console.log(`Searching for files in ${dir}`);

const config = {
    pages: [],
    destination: process.cwd()
};

for (const { current: i, skip: next } of iterSync.peekable(process.argv.slice(2)))
    if (i == '--page' || i == '-p')
        config.pages.push(next());
        
    else if (i == '--out' || i == '-o')
        config.destination = next();
        
    else
        throw `Unrecognised option '${i}'`;

for (const generator of config.pages)
    for (const [a, i] of Object.entries(req(['./', '../', '/', '#'].some(i => generator.startsWith(i)) ? generator : `${dir}/${generator}`)))
        if (typeof i == 'function') {
            console.log(`Building: ${generator}::${a}`);
            
            const page = await i();
            const out = await fs.open("")
        }
