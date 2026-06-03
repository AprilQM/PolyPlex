// composables/url.js
export const useUrlUtils = (router) => {
    const jump = (url) => {
        router.push(url)
    }
    
    const replace = (url) => {
        router.replace(url)
    }
    
    return { jump, replace }
}