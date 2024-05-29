import { Awaitable } from '@antfu/utils';
import { CustomIconLoader } from './types.cjs';

declare function FileSystemIconLoader(dir: string, transform?: (svg: string) => Awaitable<string>): CustomIconLoader;

export { FileSystemIconLoader };
