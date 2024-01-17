// pages/index.js

import React from 'react';
import Head from 'next/head';

const Home = () => {
    return (
        <div className="container mx-auto p-4">
            <Head>
                <title>Next.js & Tailwind CSS</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <main>
                <h1 className="text-4xl font-bold mb-4">Welcome</h1>
                <p className="text-lg text-gray-600">International Recipes by Country</p>

                <div className="mt-8">
                    <a
                        href="https://nextjs.org/docs"
                        className="text-blue-500 hover:underline"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Next.js Docs
                    </a>
                    <span className="mx-2">•</span>
                    <a
                        href="https://tailwindcss.com/docs"
                        className="text-blue-500 hover:underline"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Tailwind CSS Docs
                    </a>
                </div>
            </main>

            <footer className="mt-8">
                <p className="text-sm text-gray-500">&copy; 2024 Kaan</p>
            </footer>
        </div>
    );
};

export default Home;
