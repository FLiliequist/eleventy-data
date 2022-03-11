module.exports = function(elevntyConfig) {
  elevntyConfig.addPassthroughCopy("images");
  elevntyConfig.addPassthroughCopy("admin");
  elevntyConfig.addPassthroughCopy('css');
  return {
    passthroughFileCopy: true
  }
};