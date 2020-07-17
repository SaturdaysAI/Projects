//gulpfile.js
const gulp = require('gulp'),
    minifyCSS = require('gulp-clean-css'),
    uglify = require('gulp-uglify'),
    rename = require("gulp-rename"),
    sass = require('gulp-sass'),
    npmDist = require('gulp-npm-dist');

const sassFiles = 'src/assets/scss/*.scss',
    cssDest = 'dist/css/';

//compile scss into css
function style() {
    return gulp.src(sassFiles)
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest(cssDest));
}

//This is for the minify css
async function minifycss() {
    return gulp.src(['dist/css/*.css', '!dist/css/**/*.min.css'])
        .pipe(rename({
            suffix: '.min'
        }))
        .pipe(minifyCSS())
        .pipe(gulp.dest(cssDest));
}

// This is for the minifyjs
async function minifyjs() {
    return gulp.src(['dist/js/custom.js','dist/js/app.js', '!dist/js/custom.min.js',  '!dist/js/app.min.js'] )
        .pipe(rename({
            suffix: '.min'
        }))
        .pipe(uglify())
        .pipe(gulp.dest('dist/js'));
}

// Copy dependencies to ./public/libs/
async function copy() {
    gulp.src(npmDist(), {
            base: './node_modules'
        })
        .pipe(gulp.dest('./src/assets/libs'));
};

async function watch() {
    gulp.watch(['src/assets/scss/**/*.scss'], style);
    gulp.watch(['dist/css/style.css'], minifycss);
    gulp.watch(['dist/js/**/*.js', '!dist/js/**/*.min.js'], minifyjs);
}


gulp.task('default', watch);

exports.style = style;
exports.minifycss = minifycss;
exports.minifyjs = minifyjs;
exports.copy = copy;
exports.watch = watch;